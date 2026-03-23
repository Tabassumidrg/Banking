---
description: How to set up and work with the Neon PostgreSQL database for the Banking project
---

# Database (Neon PostgreSQL) Skill

## Overview
The Banking project uses **Neon** as a serverless PostgreSQL provider. All database files live in `d:\saif\Banking\db\`.

## Neon Setup
1. Go to [neon.tech](https://neon.tech) and create a project
2. Copy the connection string (format: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require`)
3. Store the connection string in environment variables (never commit to git)

## Folder Structure
```
db/
├── README.md
├── schema.sql          # Table definitions
├── migrations/         # Migration scripts
├── seed.sql            # Initial seed data
└── queries/            # Reusable SQL queries
```

## Key Commands
- Connect via psql: `psql "your_connection_string"`
- Run schema: `psql "your_connection_string" -f db/schema.sql`
- Run seeds: `psql "your_connection_string" -f db/seed.sql`

## Best Practices
- Always use parameterized queries to prevent SQL injection
- Use migrations for schema changes in production
- Keep connection strings in `.env` files, never hardcode
