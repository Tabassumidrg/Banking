---
description: How to work with the Next.js frontend section of the Banking project
---

# Frontend Section (Next.js on Vercel)

## Overview
- **Framework:** Next.js
- **Styling:** Plain HTML/CSS preferred (minimal framework-specific styling)
- **Deployment:** Vercel
- **Project folder:** `c:\Users\govtitigadag\Desktop\Banking\frontend\`
- **Token location:** `c:\Users\govtitigadag\Desktop\Banking\tokens` (line 6-7)

## Folder Structure
```
frontend/
├── public/              # Static assets (images, icons)
├── src/
│   ├── app/             # Next.js App Router pages
│   ├── components/      # Reusable UI components
│   ├── styles/          # Global and component CSS files
│   └── lib/             # Utility functions, API client
├── next.config.js
├── package.json
└── README.md
```

## Key Conventions
1. **Use plain HTML/CSS** for styling wherever possible — avoid CSS-in-JS or Tailwind unless explicitly needed.
2. CSS files live in `src/styles/` and are imported into components.
3. Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`).
4. Keep components small and focused.
5. API calls to the FastAPI backend go through helper functions in `src/lib/api.ts`.

## Deployment to Vercel
1. Connect the `frontend/` folder to Vercel.
2. Vercel auto-detects Next.js and builds accordingly.
3. Set environment variables (API base URL, etc.) in Vercel dashboard.

## Workflow
1. Set up pages in `src/app/`.
2. Build reusable components in `src/components/`.
3. Write CSS in `src/styles/`.
4. Wire API calls through `src/lib/api.ts`.
5. Test locally with `npm run dev`, deploy via Vercel.
