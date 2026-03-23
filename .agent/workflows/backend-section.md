---
description: How to work with the FastAPI backend section of the Banking project
---

# Backend Section (FastAPI on Render)

## Overview
- **Framework:** FastAPI (Python)
- **Deployment:** Render
- **Project folder:** `c:\Users\govtitigadag\Desktop\Banking\backend\`
- **Token location:** `c:\Users\govtitigadag\Desktop\Banking\tokens` (line 14-15)

## Folder Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── models/          # SQLAlchemy / Pydantic models
│   ├── routers/         # API route handlers
│   ├── services/        # Business logic layer
│   ├── schemas/         # Pydantic request/response schemas
│   ├── config.py        # Settings & env vars
│   └── database.py      # DB connection setup (Neon)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
└── README.md
```

## Key Conventions
1. Use async endpoints wherever possible.
2. Follow RESTful naming: `/api/v1/resource`.
3. Separate concerns: routers → services → models.
4. Use Pydantic for all request/response validation.
5. Store secrets in `.env`, load via `python-dotenv` or FastAPI settings.

## Deployment to Render
1. Render watches the `backend/` directory.
2. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Set environment variables in Render dashboard (DB connection string, etc.).

## Workflow
1. Define models in `models/`.
2. Create Pydantic schemas in `schemas/`.
3. Implement business logic in `services/`.
4. Wire up routes in `routers/`.
5. Register routers in `main.py`.
