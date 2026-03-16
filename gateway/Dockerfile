FROM golang:1.24 AS build

WORKDIR /app
COPY go.mod .
COPY main.go .
COPY static ./static
RUN go build -o gateway .

FROM debian:bookworm-slim

WORKDIR /app
COPY --from=build /app/gateway .
COPY --from=build /app/static ./static
ENV GATEWAY_PORT=8080
CMD ["./gateway"]
