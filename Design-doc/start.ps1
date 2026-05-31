# Start Content Hub V2 web app — backend (FastAPI :8765) + frontend (Vite :5173)
# Run from anywhere; resolves repo root from this script's location.

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot   = Split-Path -Parent $scriptDir

$venvPython   = Join-Path $repoRoot ".venv\Scripts\python.exe"
$nodeModules  = Join-Path $repoRoot "Design-doc\web\node_modules"
$webDir       = Join-Path $repoRoot "Design-doc\web"

# --- preflight ---
if (-not (Test-Path $venvPython)) {
    Write-Error "Missing repo-root .venv. Run: .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}
if (-not (Test-Path $nodeModules)) {
    Write-Error "Missing Design-doc\web\node_modules. Run: cd Design-doc\web && npm install"
    exit 1
}

# --- launch backend ---
$backendCmd = "& '$venvPython' -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$repoRoot'; $backendCmd"

# --- launch frontend ---
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$webDir'; npm run dev"

Write-Host ""
Write-Host "Servers starting..."
Write-Host "  Backend health : http://localhost:8765/api/health"
Write-Host "  Frontend app   : http://localhost:5173"
