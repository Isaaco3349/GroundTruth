# Deploy GroundTruth on Vercel (multi service)

Two services in one project: **web** (Vite UI) and **api** (FastAPI agent).

## Service layout (confirm this matches your intent)

| Service | Folder | Public? | Path |
|---------|--------|---------|------|
| **web** | `apps/web` | Yes | `/` (all pages except `/api/*`) |
| **api** | repo root | Yes | `/api/*` via rewrite |

**Bindings:** none. The browser calls `/api/health` and `/api/runs` on the same domain. That is not a server side call from the web service, so Vercel service bindings are not required.

Vercel’s auto suggestion sent all traffic to FastAPI only. That would hide the UI. This repo uses `/api/*` → api and everything else → web.

## Walkthrough

### 1. Push `vercel.json`

```powershell
cd C:\Users\user\groundtruth
git add vercel.json pyproject.toml docs/DEPLOY_VERCEL.md api/index.py
git commit -m "Vercel multi-service: web + FastAPI api"
git push
```

### 2. Import or redeploy on Vercel

1. [vercel.com/new](https://vercel.com/new) or open the existing project.
2. Root directory: **repository root**.
3. Vercel should read `vercel.json` services block (not the old single app layout).

### 3. Environment variables (project level, both services)

| Name | Required now |
|------|----------------|
| `TAVILY_API_KEY` | Yes (`tvly-…`) |
| `NEBIUS_BASE_URL` | Yes |
| `NEMOTRON_NANO` / `SUPER` / `ULTRA` | Yes (match Token Factory when available) |
| `NEBIUS_API_KEY` | When Nebius unblocks you |

Do **not** set `VITE_API_URL` on Vercel. Production uses same origin `/api`.

Do **not** set binding env vars yourself.

### 4. Deploy and test

- UI: `https://YOUR_PROJECT.vercel.app`
- Health: `https://YOUR_PROJECT.vercel.app/api/health`
- Run agent in UI (may take up to ~60s)

### 5. Devpost

Demo URL = main site URL above.

## Limits

- Agent runs need Tavily + pytest; allow ~60s. Upgrade plan if you hit timeouts.
- `/tmp` workspace on api service; run history may not persist across instances.

## Local dev

```powershell
# optional: vercel dev from repo root (needs Vercel CLI 48+)
vercel dev
```

Or two terminals: `uvicorn groundtruth.api:app --port 8787` and `npm run dev` in `apps/web`.
