from __future__ import annotations

import json
from typing import Any

import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

STAGE289_API = "https://stage289.onrender.com/verify"

app = FastAPI(
    title="Stage290 Verification URL UI",
    description="Human-friendly verification URL UI for Stage289 Verification API.",
    version="290.0.0",
)

templates = Jinja2Templates(directory="templates")


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    sample_manifest = {
        "execution": True,
        "identity": True,
        "timestamp": True,
        "workflow": "github-actions",
        "signer": "demo-signer",
    }
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "stage": "290",
            "sample_url": "https://example.com",
            "sample_manifest": pretty_json(sample_manifest),
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "stage": "290",
        "name": "Verification URL UI",
        "status": "ok",
    }


@app.post("/verify-ui", response_class=HTMLResponse)
def verify_ui(
    request: Request,
    url: str = Form(...),
    manifest_text: str = Form(...),
) -> HTMLResponse:
    parsed_manifest: dict[str, Any] | None = None
    parse_error: str | None = None
    api_result: dict[str, Any] | None = None
    api_error: str | None = None

    try:
        loaded = json.loads(manifest_text)
        if not isinstance(loaded, dict):
            raise ValueError("manifest must be a JSON object")
        parsed_manifest = loaded
    except Exception as exc:
        parse_error = f"{type(exc).__name__}: {exc}"

    if parse_error is None:
        payload = {
            "url": url,
            "manifest": parsed_manifest,
        }
        try:
            response = requests.post(STAGE289_API, json=payload, timeout=30)
            response.raise_for_status()
            api_result = response.json()
        except Exception as exc:
            api_error = f"{type(exc).__name__}: {exc}"

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "url": url,
            "manifest_text": manifest_text,
            "parsed_manifest": parsed_manifest,
            "parse_error": parse_error,
            "api_result": api_result,
            "api_error": api_error,
            "api_result_pretty": pretty_json(api_result) if api_result is not None else None,
        },
    )
