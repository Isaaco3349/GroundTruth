# GroundTruth

GroundTruth is a coding agent that gathers web evidence before it changes your repository, runs tests locally, and routes NVIDIA Nemotron models on Nebius Token Factory by task depth. Tavily Research supplies cited sources that appear in the UI next to every non trivial patch plan.

Built for the [Nebius x NVIDIA Global AI Hackathon](https://nebiusglobalaihackathon.devpost.com/). Devpost track: **Coding and Agentic Engineering**. The same codebase also supports a personal memory layer and a workflow people can run daily.

## Why this exists

Most coding agents guess when APIs, libraries, or error messages drift. GroundTruth treats external facts as a gate: if the evidence pack is empty or weak, the agent stops and asks for a narrower task instead of hallucinating a fix.

## Stack

| Layer | Technology |
|--------|------------|
| Inference | Nebius Token Factory (OpenAI compatible API) |
| Models | NVIDIA Nemotron Nano, Super, Ultra (open weights via Token Factory) |
| Web grounding | Tavily Search and Research |
| API | FastAPI |
| CLI | Typer + Rich |
| UI | Vite + React (Nebius lime and black theme) |

## Repository layout

```
groundtruth/
  apps/web/              Web dashboard (evidence sidebar, run log)
  assets/brand/          Color tokens and logo notes
  docs/                  Architecture, Devpost draft, sponsor feedback
  fixtures/sample_project Tiny repo with one failing test for demos
  scripts/               Demo and dev helpers
  src/groundtruth/       Agent, Nemotron router, Tavily, memory, tools
  tests/                 Unit and integration tests
```

## Prerequisites

- Python 3.11+
- Node.js 20+ (for the web UI)
- Nebius Token Factory API key (hackathon credits: activation code `NEBIUS-DEVPOST-GLOBAL26`)
- Tavily API key (Nebius Builders Program)

## Quick start

### 1. Clone and configure

```bash
git clone https://github.com/YOUR_USER/groundtruth.git
cd groundtruth
cp .env.example .env
```

Fill in `NEBIUS_API_KEY` and `TAVILY_API_KEY`. Confirm model IDs in the Nebius playground match `.env`.

### 2. Python environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

### 3. Run the sample failure

```bash
python -m groundtruth.cli --task "Fix the failing test in the sample project"
```

### 4. API server (for the web UI)

```bash
uvicorn groundtruth.api:app --reload --port 8787
```

### 5. Web UI

```bash
cd apps/web
npm install
npm run dev
```

Open the URL shown in the terminal. The UI uses Nebius brand colors documented in `assets/brand/colors.css`.

## Nemotron routing

| Stage | Typical model | Role |
|--------|----------------|------|
| Classify task | Nano | Cheap routing, risk level, tool choice |
| Patch and edit | Super | Multi file code changes |
| Architecture and high risk refactors | Ultra | Deep reasoning (use sparingly for credits) |

The router logs latency and token usage under `data/runs/` for README tables and demo video.

## Tavily usage

1. **Research** with a JSON schema produces an `EvidencePack` (claims, sources, risks).
2. **Search** (`advanced` depth) finds official docs when Research is overkill.
3. Cached evidence under `data/evidence_cache/` keeps demos stable and saves credits.

See `docs/architecture.md` for the full loop.

## Without Nebius yet

If `NEBIUS_API_KEY` is empty, the agent still runs Tavily evidence, applies the sample project fallback patch, and runs pytest. Add the Token Factory key when access works and the same loop uses Nemotron without structural changes.

See `docs/nigeria_nebius_path.md` if billing country blocks signup.

## Hackathon submission checklist

- [ ] Working demo URL or CLI recording
- [ ] Public GitHub with this README
- [ ] YouTube demo (3 minutes or less)
- [ ] Devpost description (draft in `docs/devpost_draft.md`)
- [ ] Feedback on Nebius and Tavily (`docs/nebius_feedback.md`, `docs/tavily_feedback.md`)

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

NVIDIA Nemotron on Nebius Token Factory, Tavily, and the Nebius x NVIDIA Global AI Hackathon organizers.
