---
description: How to set up and work with the Next.js frontend for the Banking project
---

# Frontend (Next.js on Vercel) Skill

## Overview
The Banking project frontend is built with **Next.js** and deployed on **Vercel**. HTML/CSS is used wherever possible for simplicity. All frontend files live in `d:\saif\Banking\frontend\`.

## Project Setup
1. Navigate to `d:\saif\Banking\frontend\`
2. Initialize Next.js: `npx -y create-next-app@latest ./`
3. Install dependencies: `npm install`

## Folder Structure
```
frontend/
├── README.md
├── package.json
├── next.config.js
├── public/                # Static assets
│   ├── images/
│   └── styles/            # Global CSS files
├── src/
│   ├── app/               # App Router pages
│   │   ├── layout.js      # Root layout
│   │   ├── page.js        # Home page
│   │   ├── globals.css    # Global styles
│   │   └── [routes]/      # Feature pages
│   ├── components/        # Reusable components (HTML/CSS focused)
│   └── lib/               # API utilities, helpers
└── .env.local             # Environment variables
```

## Key Commands
- Dev server: `npm run dev` (http://localhost:3000)
- Build: `npm run build`
- Start prod: `npm start`

## Vercel Deployment
1. Push code to GitHub
2. Import project in Vercel dashboard
3. Set root directory to `frontend/`
4. Add environment variables
5. Deploy

## Design Approach
- Use **vanilla HTML/CSS** for layout and styling wherever possible
- Use Next.js only for routing, SSR, and API calls
- Keep components simple — prefer CSS classes over CSS-in-JS
- Use CSS custom properties for theming

## Best Practices
- Use semantic HTML elements
- Keep CSS modular with CSS Modules or scoped styles
- Optimize images with `next/image`
- Use environment variables for API URLs
