---
description: How to work with the Neon PostgreSQL database section of the Banking project
---

# Database Section Workflow

## Prerequisites
- Neon API token (stored in `tokens` file at project root)
- Database connection details (stored in `db/.env`)

## Database Details
- **Project**: Banking (`aged-paper-21106693`)
- **Database**: `neondb`
- **User**: `neondb_owner`
- **Region**: `aws-us-east-1`
- **PostgreSQL Version**: 17

## Connection String
```
postgresql://neondb_owner:<password>@ep-long-grass-amjlgvmu.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Environment File
All connection details are stored in `db/.env`. Load this file in your backend application.

## Neon API Reference
- **Base URL**: `https://console.neon.tech/api/v2`
- **Auth Header**: `Authorization: Bearer <NEON_API_TOKEN>`

### Common API Calls
// turbo-all

1. **Get project info**:
```powershell
$headers = @{ "Authorization" = "Bearer $env:NEON_TOKEN" }
Invoke-WebRequest -Uri "https://console.neon.tech/api/v2/projects/aged-paper-21106693" -Headers $headers
```

2. **Check endpoints**:
```powershell
Invoke-WebRequest -Uri "https://console.neon.tech/api/v2/projects/aged-paper-21106693/endpoints" -Headers $headers
```

3. **List databases**:
```powershell
Invoke-WebRequest -Uri "https://console.neon.tech/api/v2/projects/aged-paper-21106693/databases" -Headers $headers
```
