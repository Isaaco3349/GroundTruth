# Deploy GroundTruth on Vercel

One project serves the React UI and the FastAPI agent API under `/api/*`.

## Before you deploy

1. Push latest code to GitHub (includes `vercel.json`, `api/index.py`).
2. Have **`TAVILY_API_KEY`** (`tvly-…`) ready. Do not commit `.env`.
3. **`NEBIUS_API_KEY`** optional until Token Factory works.

## Walkthrough

### 1. Import project

1. Open [vercel.com/new](https://vercel.com/new).
2. Import your **groundtruth** GitHub repository.
3. **Root directory:** leave as repository root (not `apps/web`).
4. Vercel should detect `vercel.json`. Confirm:
   - **Install:** `pip install -r requirements.txt && cd apps/web && npm install`
   - **Build:** `cd apps/web && npm run build`
   - **Output:** `apps/web/dist`

### 2. Environment variables

In **Project → Settings → Environment Variables**, add:

| Name | Value |
|------|--------|
| `TAVILY_API_KEY` | your `tvly-…` key |
| `NEMOTRON_NANO` | model id from Token Factory playground |
| `NEMOTRON_SUPER` | model id |
| `NEMOTRON_ULTRA` | model id |
| `NEBIUS_API_KEY` | leave empty until Nebius unblocks you |
| `NEBIUS_BASE_URL` | `https://api.tokenfactory.nebius.com/v1/` |

Apply to **Production** (and Preview if you want).

Do not set `VITE_API_URL` on Vercel. Production uses same origin `/api`.

### 3. Deploy

Click **Deploy**. First build may take a few minutes (Python + Node).

### 4. Verify live site

1. Open `https://YOUR_PROJECT.vercel.app`.
2. You should see the GroundTruth UI (lime header).
3. Click **Run agent** with the default task.
4. Expect Tavily sources in the right panel and **completed** in the log after ~30–60s.

API checks:

- `https://YOUR_PROJECT.vercel.app/api/health`

### 5. Devpost demo URL

Use the main site URL: `https://YOUR_PROJECT.vercel.app`

## Limits

- Serverless **max duration is 60s** on this config. Tavily + pytest usually fit; slow Research may timeout on cold starts.
- Run history on Vercel uses `/tmp` and may not persist across instances.
- Hobby plan limits may apply; upgrade or retry if runs time out.

## Local dev (unchanged)

Terminal 1:

```powershell
cd C:\Users\user\groundtruth
$env:PYTHONPATH="src"
uvicorn groundtruth.api:app --reload --port 8787
```

Terminal 2:

```powershell
cd C:\Users\user\groundtruth\apps\web
npm run dev
```

UI calls `http://127.0.0.1:8787/api/health` and `/api/runs`.

## After Nebius access

Add `NEBIUS_API_KEY` in Vercel → **Redeploy** (or wait for next push). No code change.
