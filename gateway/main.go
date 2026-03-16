package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type healthResponse struct {
	Status  string `json:"status"`
	Service string `json:"service"`
}

func main() {
	mux := http.NewServeMux()
	staticDir := filepath.Join(".", "static")
	mux.Handle("/", staticHandler(staticDir))
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, healthResponse{Status: "ok", Service: "gateway"})
	})
	mux.HandleFunc("/v1/chat/respond", proxyJSON(os.Getenv("AI_ENGINE_URL"), "/v1/chat/respond"))
	mux.HandleFunc("/v1/chat/knowledge", proxyJSON(os.Getenv("AI_ENGINE_URL"), "/v1/chat/knowledge"))
	mux.HandleFunc("/v1/chat/library/status", proxyJSON(os.Getenv("AI_ENGINE_URL"), "/v1/chat/library/status"))
	mux.HandleFunc("/v1/themes", proxyJSON(os.Getenv("AI_ENGINE_URL"), "/v1/themes/"))
	mux.HandleFunc("/v1/themes/generate", proxyJSON(os.Getenv("AI_ENGINE_URL"), "/v1/themes/generate"))

	port := firstNonEmpty(os.Getenv("PORT"), os.Getenv("GATEWAY_PORT"), "8080")
	server := &http.Server{
		Addr:              ":" + port,
		Handler:           withCORS(loggingMiddleware(mux)),
		ReadHeaderTimeout: 5 * time.Second,
	}

	log.Printf("gateway listening on %s", server.Addr)
	log.Fatal(server.ListenAndServe())
}

func staticHandler(staticDir string) http.Handler {
	fileServer := http.FileServer(http.Dir(staticDir))

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch filepath.Ext(r.URL.Path) {
		case "", ".html", ".js", ".css", ".webmanifest", ".svg":
			w.Header().Set("Cache-Control", "no-store, no-cache, must-revalidate")
			w.Header().Set("Pragma", "no-cache")
			w.Header().Set("Expires", "0")
		}
		fileServer.ServeHTTP(w, r)
	})
}

func proxyJSON(baseURL, path string) http.HandlerFunc {
	client := &http.Client{Timeout: 20 * time.Second}
	targetBase := normalizeBaseURL(getenvWithValue(baseURL, "http://localhost:8000"))

	return func(w http.ResponseWriter, r *http.Request) {
		target := targetBase + path
		if r.URL.RawQuery != "" {
			target += "?" + r.URL.RawQuery
		}
		var body io.Reader

		if r.Body != nil {
			rawBody, _ := io.ReadAll(r.Body)
			body = bytes.NewReader(rawBody)
		}

		req, err := http.NewRequest(r.Method, target, body)
		if err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		req.Header.Set("Content-Type", "application/json")

		resp, err := client.Do(req)
		if err != nil {
			writeJSON(w, http.StatusBadGateway, map[string]string{"error": err.Error()})
			return
		}
		defer resp.Body.Close()

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	}
}

func withCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(start))
	})
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func getenv(key, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}
	return value
}

func getenvWithValue(value, fallback string) string {
	if value == "" {
		return fallback
	}
	return value
}

func firstNonEmpty(values ...string) string {
	for _, value := range values {
		if value != "" {
			return value
		}
	}
	return ""
}

func normalizeBaseURL(value string) string {
	if value == "" {
		return "http://localhost:8000"
	}
	if strings.HasPrefix(value, "http://") || strings.HasPrefix(value, "https://") {
		return value
	}
	return "http://" + value
}
