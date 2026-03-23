---
description: How to set up and work with the FastAPI backend for the Banking project
---

# Backend (FastAPI on Render) Skill

## Overview
The Banking project backend is built with **FastAPI** (Python) and deployed on **Render**. All backend files live in `d:\saif\Banking\backend\`.

## Project Setup
1. Navigate to `d:\saif\Banking\backend\`
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Folder Structure
```
backend/
├── README.md
├── main.py                # FastAPI app entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── database.py        # Neon DB connection
│   ├── models/            # SQLAlchemy/Pydantic models
│   ├── routes/            # API route handlers
│   ├── services/          # Business logic
│   └── middleware/        # Auth, CORS, etc.
└── tests/                 # Test files
```

## Key Commands
- Run dev server: `uvicorn main:app --reload`
- API docs: `http://localhost:8000/docs`
- Run tests: `pytest`

## Render Deployment
1. Push code to GitHub
2. Create a new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

## Best Practices
- Use Pydantic models for request/response validation
- Keep routes thin, put logic in services
- Use dependency injection for database sessions
- Always add CORS middleware for frontend connectivity
