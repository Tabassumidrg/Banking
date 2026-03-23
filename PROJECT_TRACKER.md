# 🏦 Banking Project - Detailed Project Document

## Project Overview

A full-stack banking application built with a modern architecture:

| Layer | Technology | Hosting |
|-------|-----------|---------|
| **Frontend** | Next.js (HTML/CSS where possible) | Vercel |
| **Backend** | FastAPI (Python) | Render |
| **Database** | PostgreSQL | Neon |

---

## Project Structure

```
Banking/
├── frontend/     # Next.js app (deployed on Vercel)
├── backend/      # FastAPI app (deployed on Render)
├── db/           # Database schemas, migrations, seed data
├── .agents/      # Skills for each project section
│   └── workflows/
└── PROJECT_TRACKER.md  (this file)
```

---

## Progress Tracker

### Phase 1: Project Setup
- [x] Create folder structure (`db/`, `backend/`, `frontend/`)
- [x] Create project tracking document

### Phase 2: Database Setup (Neon PostgreSQL)
- [ ] Design database schema
- [ ] Set up Neon project
- [ ] Create tables and relationships
- [ ] Seed initial data

### Phase 3: Backend Setup (FastAPI on Render)
- [ ] Initialize FastAPI project
- [ ] Set up database connection (Neon)
- [ ] Define API endpoints
- [ ] Add authentication
- [ ] Deploy to Render

### Phase 4: Frontend Setup (Next.js on Vercel)
- [ ] Initialize Next.js project
- [ ] Build pages with HTML/CSS
- [ ] Connect to backend API
- [ ] Deploy to Vercel

---

## Decisions & Notes

| Date | Decision | Details |
|------|----------|---------|
| 2026-03-23 | Project initialized | Created 3-folder structure: `db/`, `backend/`, `frontend/` |

---

*Last updated: 2026-03-23*
