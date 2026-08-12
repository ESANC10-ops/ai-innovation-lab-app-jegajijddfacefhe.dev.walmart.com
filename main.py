#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import os

app = FastAPI(title="Merchant Dashboard", version="1.0.0")
BASE_DIR = Path(__file__).parent

@app.middleware("http")
async def no_cache(request, call_next):
    response = await call_next(request)
    if request.url.path.endswith(('.html', '.json')):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.get("/", response_class=HTMLResponse)
async def root():
    p = BASE_DIR / "merchant.html"
    return FileResponse(p) if p.exists() else "<h1>merchant.html not found</h1>"

@app.get("/{path:path}")
async def serve(path: str):
    p = BASE_DIR / path
    if p.exists() and p.is_file():
        return FileResponse(p)
    return {"error": "Not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
