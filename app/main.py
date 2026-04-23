from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from typing import Any

import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

STAGE289_API = "https://stage289.onrender.com/verify"

app = FastAPI(
    title="Stage290 Verification URL UI",
    description="Human-friendly verification URL UI for Stage289 Verification API.",
    version="290.2.0",
)

templates = Jinja2Templates(directory="templates")

# 簡易メモリ保存
# Render free環境では永続化されない可能性がありますが、
# まずは共有URLの体験を作るための最小実装です。
RESULT_STORE: dict[str, dict[str, Any]] = {}


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def now_iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_share_url(request: Request, verification_id: str) -> str:
    return str(request.url_for("result_by_id", verification_id=verification_id))


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


@app.get("/result/{verification_id}", response_class=HTMLResponse, name="result_by_id")
def result_by_id(request: Request, verification_id: str) -> HTMLResponse:
    stored = RESULT_STORE.get(verification_id)

    if stored is None:
        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "verification_id": verification_id,
                "verified_at": None,
                "share_url": None,
                "url": None,
                "manifest_text": None,
                "parsed_manifest": None,
                "parse_error": None,
                "api_result": None,
                "api_error": f"Verification result '{verification_id}' was not found.",
                "api_result_pretty": None,
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "verification_id": verification_id,
            "verified_at": stored["verified_at"],
            "share_url": build_share_url(request, verification_id),
            "url": stored["url"],
            "manifest_text": stored["manifest_text"],
            "parsed_manifest": stored["parsed_manifest"],
            "parse_error": stored["parse_error"],
            "api_result": stored["api_result"],
            "api_error": stored["api_error"],
            "api_result_pretty": pretty_json(stored["api_result"]) if stored["api_result"] is not None else None,
        },
    )


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

    verification_id = secrets.token_urlsafe(8)
    verified_at = now_iso_utc()

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

    RESULT_STORE[verification_id] = {
        "verified_at": verified_at,
        "url": url,
        "manifest_text": manifest_text,
        "parsed_manifest": parsed_manifest,
        "parse_error": parse_error,
        "api_result": api_result,
        "api_error": api_error,
    }

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "verification_id": verification_id,
            "verified_at": verified_at,
            "share_url": build_share_url(request, verification_id),
            "url": url,
            "manifest_text": manifest_text,
            "parsed_manifest": parsed_manifest,
            "parse_error": parse_error,
            "api_result": api_result,
            "api_error": api_error,
            "api_result_pretty": pretty_json(api_result) if api_result is not None else None,
        },
    )
