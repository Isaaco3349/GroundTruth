# API keys setup

No credit card is required for hackathon credits if you follow the promo and Builders paths below.

## Nebius Token Factory (~$50 total possible)

### Step A: Hackathon $25

1. Open [Devpost Resources](https://nebiusglobalaihackathon.devpost.com/resources).
2. Submit the **Token Factory credits** form.
3. Use activation code **`NEBIUS-DEVPOST-GLOBAL26`** in the form (exact spelling).
4. Create or sign in to [Nebius Token Factory](https://docs.tokenfactory.nebius.com/api-reference/introduction).
5. In Token Factory: click your **balance** → **Top up** → **Apply promo code** → enter the code you received.
6. Create an API key: **API keys** → **Create API key** → save it once (you cannot view it again).
7. Put the key in `.env` as `NEBIUS_API_KEY`.

Promo codes work without billing or a bank card. See [Token Factory billing docs](https://docs.tokenfactory.nebius.com/other-capabilities/billing).

### Step B: Builders Program another $25

1. Join free at [dev.nebius.com/builders](https://dev.nebius.com/builders).
2. Verify email (double opt in). Membership is inactive until verified.
3. Claim Token Factory credits from the dashboard (second $25 code or auto grant per current program terms).
4. Redeem on the same Token Factory account balance.

## Tavily ($25 via Builders)

1. Complete Builders signup and email verification (same as Step B above).
2. Follow Tavily onboarding for Nebius builders: [tavily.com/nebius-builders](https://www.tavily.com/nebius-builders). Credits are applied automatically; no card required.
3. Create a Tavily API key in the Tavily dashboard.
4. Put it in `.env` as `TAVILY_API_KEY`.

## Tavily CLI setup (recommended)

Follow [Tavily agent setup](https://www.tavily.com/agent-setup/SKILL.md):

1. `pip install tavily-cli` then `tvly login` (browser OAuth, no manual key copy for CLI).
2. From the repo root: `python scripts/sync_tavily_env.py` copies credentials into `.env` for the FastAPI app.

## Verify locally

```bash
cp .env.example .env
python scripts/sync_tavily_env.py

python -c "from groundtruth.config import get_settings; s=get_settings(); print('nebius', bool(s.nebius_api_key), 'tavily', bool(s.tavily_api_key))"
```

After keys work, run a minimal Nemotron call from the playground model ID, then Phase 1 in `docs/roadmap.md`.

## If credits are delayed

| Symptom | What to do |
|---------|------------|
| Form submitted, no email | Check spam; wait 24h; ask in [Nebius Discord](https://nebiusglobalaihackathon.devpost.com/resources) (link on Resources page). |
| Promo rejected | Confirm code `NEBIUS-DEVPOST-GLOBAL26`; apply under balance → Top up → Apply promo code. |
| Builders pending | Finish email verification; avoid disposable email domains. |
| Balance zero | Token Factory menu balance must be positive or API returns errors. |

## Security

Never commit `.env`. Never put Nebius or Tavily keys in the web client. Keys stay on the FastAPI server only.
