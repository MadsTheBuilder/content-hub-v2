# Design-doc Web App

## Quickstart

From the repo root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd Design-doc\web
npm install
```

Start the backend from the repo root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload
```

Start the frontend from `Design-doc/web/`:

```powershell
npm run dev
```

Open `http://localhost:5173`.
