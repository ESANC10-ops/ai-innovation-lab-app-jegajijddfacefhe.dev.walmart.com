#!/usr/bin/env python3

from fastapi import FastAPI, StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import os

app = FastAPI(
    title="Merchant Dashboard",
    description="Hiper Sur - El Viaje del Merchant",
    version="1.0.0"
)

BASE_DIR = Path(__file__).parent

@app.middleware("http")
async def add_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path.endswith(('.html', '.json')):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

@app.get("/", response_class=HTMLResponse)
async def root():
    merchant_path = BASE_DIR / "merchant.html"
    if merchant_path.exists():
        return FileResponse(merchant_path, media_type="text/html")
    return "<h1>merchant.html no encontrado</h1>"

@app.get("/merchant.html", response_class=HTMLResponse)
async def merchant():
    merchant_path = BASE_DIR / "merchant.html"
    if merchant_path.exists():
        return FileResponse(merchant_path, media_type="text/html")
    return "<h1>merchant.html no encontrado</h1>"

@app.get("/health")
async def health():
    from datetime import datetime
    return {
        "status": "healthy",
        "app": "merchant-dashboard",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
async def info():
    merchant_path = BASE_DIR / "merchant.html"
    json_files = len(list(BASE_DIR.glob("*.json")))
    return {
        "name": "El Viaje del Merchant - Hiper Sur",
        "version": "1.0.0",
        "merchant_html_exists": merchant_path.exists(),
        "json_files": json_files,
        "base_dir": str(BASE_DIR)
    }

@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    file_full_path = BASE_DIR / file_path
    try:
        file_full_path = file_full_path.resolve()
        if not str(file_full_path).startswith(str(BASE_DIR.resolve())):
            return {"error": "Acceso denegado"}
        if file_full_path.exists() and file_full_path.is_file():
            return FileResponse(file_full_path)
    except:
        pass
    return {"error": f"Archivo no encontrado: {file_path}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
