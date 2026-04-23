# Stage290: Verification URL UI

## Overview

Stage290 adds a human-friendly verification URL interface on top of Stage289.

Stage289 provides:
- decision
- trust score
- evidence
- API output

Stage290 adds:
- browser input form
- readable result page
- human-facing verification flow

This stage turns:
- Verification API
into:
- Verification service UI

---

## Architecture

User
→ Stage290 UI
→ Stage289 Verification API
→ Result page

---

## Routes

- `GET /` : input form
- `POST /verify-ui` : submit verification request
- `GET /health` : health check

---

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000
Public Positioning

Stage289:

machine-readable verification API

Stage290:

human-readable verification URL UI
License

MIT License
