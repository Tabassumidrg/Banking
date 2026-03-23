# 🏦 Banking Application — Project Tracker

> **Started:** 2026-03-23  
> **Stack:** Next.js (Vercel) · FastAPI (Render) · PostgreSQL (Neon)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                      Vercel                         │
│              Next.js Frontend                       │
│         (HTML/CSS focused styling)                  │
└───────────────────────┬─────────────────────────────┘
                        │  REST API calls
                        ▼
┌─────────────────────────────────────────────────────┐
│                      Render                         │
│              FastAPI Backend                        │
└───────────────────────┬─────────────────────────────┘
                        │  SQL queries
                        ▼
┌─────────────────────────────────────────────────────┐
│                       Neon                          │
│              PostgreSQL Database                    │
└─────────────────────────────────────────────────────┘
```

---

## Project Structure

```
Banking/
├── db/                  # Neon PostgreSQL — schemas, migrations, seeds
├── backend/             # Render FastAPI — API endpoints, models, services
├── frontend/            # Vercel Next.js — pages, components (HTML/CSS focus)
├── tokens               # API keys (GitHub, Vercel, Neon, Render)
└── PROJECT_TRACKER.md   # This file — living project document
```

---

## Steps Log

### Phase 0 — Project Setup ✅
| # | Step | Status | Date |
|---|------|--------|------|
| 1 | Finalize project structure (db / backend / frontend) | ✅ Done | 2026-03-23 |
| 2 | Create project tracker document | ✅ Done | 2026-03-23 |
| 3 | Store API tokens (GitHub, Vercel, Neon, Render) | ✅ Done | 2026-03-23 |

### Phase 1 — Database (Neon PostgreSQL)
| # | Step | Status | Date |
|---|------|--------|------|
| | _Steps will be added as we finalize them_ | | |

### Phase 2 — Backend (FastAPI on Render)
| # | Step | Status | Date |
|---|------|--------|------|
| | _Steps will be added as we finalize them_ | | |

### Phase 3 — Frontend (Next.js on Vercel)
| # | Step | Status | Date |
|---|------|--------|------|
| | _Steps will be added as we finalize them_ | | |

### Phase 4 — Integration & Deployment
| # | Step | Status | Date |
|---|------|--------|------|
| | _Steps will be added as we finalize them_ | | |

---

## Decisions & Notes

- **Frontend styling:** Prefer plain HTML/CSS wherever possible over framework-specific styling.
- **Deployment:** Frontend → Vercel, Backend → Render, Database → Neon.
- **Tokens:** Stored locally in `tokens` file (not committed to git).
