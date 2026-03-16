$ErrorActionPreference = "Stop"

Write-Host "Start services in separate terminals:"
Write-Host "1. cd ai-engine; python -m venv .venv; .venv\\Scripts\\activate; pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000"
Write-Host "2. cd events; npm install; npm run dev"
Write-Host "3. cd gateway; go run ."
Write-Host "4. cd web; npm install; npm run dev"

