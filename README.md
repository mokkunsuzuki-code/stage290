# Stage290: Verification URL UI

## Overview

Stage290 transforms the Stage289 Verification API into a **human-friendly verification URL interface**.

Users can input a URL and a manifest, then receive:

- Decision (accept / pending / reject)
- Trust score
- Trust breakdown (Integrity / Execution / Identity / Time)
- Verification ID
- Timestamp
- Shareable result URL

This stage converts:

Verification API → Verification Experience

---

## Key Features

### 1. Human-Friendly Verification UI
No terminal or JSON parsing required.

### 2. Shareable Verification Result
Each verification produces a unique:

- Verification ID
- Timestamp
- Public result URL

Example:


https://stage290.onrender.com/result/
<verification_id>


---

### 3. Trust Model Visualization

The system evaluates:

- Integrity (hash / evidence)
- Execution (workflow / CI)
- Identity (signer / key)
- Time (timestamp / reproducibility)

Final decision:

- ACCEPT
- PENDING
- REJECT

---

### 4. Fail-Closed Design

If verification is incomplete or invalid:

→ system does NOT accept  
→ explicit reject or pending

---

## Architecture


User (Browser)
↓
Stage290 UI
↓
Stage289 Verification API
↓
Decision + Evidence
↓
Human-readable result page


---

## API Dependency

This stage depends on:

Stage289 Verification API


POST /verify


---

## Example Flow

1. Enter URL + manifest
2. Click "Verify"
3. System calls Stage289 API
4. Result page generated
5. Shareable URL issued

---

## Why This Matters

Previous stages proved:

- verification
- reproducibility
- public exposure

Stage290 adds:

- usability
- accessibility
- shareability

This is the step from:

Technical validation → Product experience

---

## Limitations (Important)

Current implementation:

- Results stored in memory (temporary)
- May reset on server restart

Next stage:

Stage291 → Persistent verification records

---

## License

MIT License (2025)
