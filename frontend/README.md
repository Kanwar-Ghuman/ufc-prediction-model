# Octagon — website

Next.js front end for `../model`. Numbers come from the FastAPI service;
this app does not train or score fights.

```bash
cd ../model && uv run python -m octagon serve   # http://127.0.0.1:8000
npm install && npm run dev                      # http://localhost:3000
```

`NEXT_PUBLIC_API_BASE` (see `.env.local.example`) defaults to
`http://127.0.0.1:8000`. If the API is down, pages say so instead of
showing zeros.

| Route | Content |
| --- | --- |
| `/` | Next UFC card |
| `/cards` | Cards with frozen predictions |
| `/cards/[slug]` | One card, plus the scorecard after results land |
| `/results` | Holdout metrics and reliability curves |
