$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "Starting Kumar Nikhil AI CV stack..." -ForegroundColor Cyan
docker compose up -d --build

Write-Host ""
Write-Host "Application URL: http://localhost:8080" -ForegroundColor Green
Write-Host "API URL: http://localhost:8000" -ForegroundColor Green
Write-Host "Events URL: http://localhost:8081" -ForegroundColor Green
