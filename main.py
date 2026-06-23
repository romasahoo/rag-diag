"""
RAG-Diag — FastAPI Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
AI-powered hardware diagnostics engine with a simulated RAG pipeline.

Endpoints:
  GET  /              → Serves the main SPA
  POST /api/diagnose  → Runs the diagnostic and returns JSON results
  GET  /api/systems   → Returns available hardware systems
"""

import re
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from knowledge_base import SYSTEMS, generate_fallback, lookup_diagnostic

# ─── App Setup ─── #

app = FastAPI(
    title="RAG-Diag",
    description="AI Hardware Diagnostics Engine",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ─── Routes ─── #

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main single-page application."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/systems")
async def get_systems():
    """Return the list of available hardware systems."""
    systems = [
        {"key": key, "name": data["name"]}
        for key, data in SYSTEMS.items()
    ]
    return {"systems": systems}


@app.post("/api/diagnose")
async def diagnose(request: Request):
    """
    Run a diagnostic sequence for the given hardware system and error code.

    Expects JSON body:
        {
            "system": "ebike" | "washer" | "smarthome",
            "error_code": "E01" | "F18" | "503" | ...
        }

    Returns the full diagnostic result including issue, steps, warning,
    confidence score, and simulated RAG context sources.
    """
    body = await request.json()
    system_key = body.get("system", "").strip()
    error_code_raw = body.get("error_code", "").strip()

    # Validation
    if not system_key or system_key not in SYSTEMS:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid or missing hardware system."},
        )

    if not error_code_raw:
        return JSONResponse(
            status_code=400,
            content={"error": "Error code or symptom is required."},
        )

    # Lookup or generate fallback
    result = lookup_diagnostic(system_key, error_code_raw)
    if result is None:
        result = generate_fallback(system_key, error_code_raw)

    system_name = SYSTEMS[system_key]["name"]

    return {
        "system_name": system_name,
        "error_code": error_code_raw.upper(),
        "confidence": result["confidence"],
        "issue": result["issue"],
        "steps": result["steps"],
        "warning": result["warning"],
        "sources": result["sources"],
    }


# ─── Run with Uvicorn ─── #

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
