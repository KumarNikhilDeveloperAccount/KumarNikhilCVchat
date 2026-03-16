$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "Container status" -ForegroundColor Cyan
docker compose ps

Write-Host ""
Write-Host "Gateway health" -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get
    $health | ConvertTo-Json
} catch {
    Write-Host "Gateway is not responding on http://localhost:8080/health" -ForegroundColor Yellow
}
