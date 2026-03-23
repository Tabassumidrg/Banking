---
description: How to work with the Neon PostgreSQL database section of the Banking project
---

# Database Section (Neon PostgreSQL)

## Overview
- **Service:** Neon (serverless PostgreSQL)
- **Project folder:** `c:\Users\govtitigadag\Desktop\Banking\db\`
- **Token location:** `c:\Users\govtitigadag\Desktop\Banking\tokens` (line 10-11)

## Folder Structure
```
db/
├── schemas/         # SQL table definitions
├── migrations/      # Incremental schema changes
├── seeds/           # Sample/initial data
└── README.md        # DB-specific docs
```

## Key Conventions
1. All SQL files use lowercase snake_case naming.
2. Migrations are numbered sequentially: `001_create_users.sql`, `002_create_accounts.sql`, etc.
3. Every table must include `created_at` and `updated_at` timestamp columns.
4. Use UUID for primary keys where appropriate.

## Connection
- Neon provides a connection string in the dashboard.
- The backend connects to Neon via the connection string stored as an environment variable.

## Workflow
1. Design schema in `schemas/` folder first.
2. Create corresponding migration files in `migrations/`.
3. Add seed data in `seeds/` if needed.
4. Test locally or against Neon directly.
