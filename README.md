# Kumar Nikhil AI CV

This workspace currently runs Kumar Nikhil's AI Chat CV as the active product experience.

Core services:

- a Go gateway serving the live UI and proxying API calls
- a FastAPI AI engine answering from Kumar Nikhil's CV
- a Node.js event service
- a React web scaffold and Flutter mobile scaffold for later expansion

## Run Locally

The repo is configured to run in `mock` mode by default so you can use the product without paid services on day 1.

## Fastest Path Right Now

If Docker Desktop is available, the simplest working path is:

```powershell
docker compose up -d
```

Then open `http://localhost:8080`.

The Go gateway serves the current live CV UI directly and proxies the AI engine.

## Tomorrow Restart

If you switch off the laptop, the app will stop. Tomorrow, start it again with either:

```powershell
docker compose up -d
```

or:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-kumar-ai-cv.ps1
```

Then open `http://localhost:8080`.

To check status:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\status-kumar-ai-cv.ps1
```

## Public Deployment

If you want a single public link that works on phones and desktops with no installation, use the Render setup included in this repo:

- [render.yaml](C:\Users\nkash\OneDrive\Documents\Playground\render.yaml)
- [DEPLOY_RENDER.md](C:\Users\nkash\OneDrive\Documents\Playground\DEPLOY_RENDER.md)

That path deploys:

- one public gateway service
- one AI engine service behind it

### 1. AI Engine

```powershell
cd ai-engine
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Event Service

```powershell
cd events
npm install
npm run dev
```

### 3. Go Gateway

```powershell
cd gateway
go run .
```

### 4. Web App

Optional for later local frontend work:

```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:5173`.

## Mock Mode

If no external model keys are configured, the AI engine uses deterministic mock responses and still exercises:

- request routing
- prompt safety logic
- memory extraction
- theme hints

## Structure

```text
gateway/    Go API gateway
ai-engine/  FastAPI model orchestrator
events/     Node.js realtime stream service
web/        React + Tailwind application
mobile/     Flutter scaffold
shared/     Shared theme schema and seed data
scripts/    Local helper scripts
```

## Branding Rules

- The active product experience is `Kumar Nikhil AI CV`
- The assistant behaves as Kumar Nikhil's official AI CV companion
