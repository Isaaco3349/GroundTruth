# Nigeria and Nebius Token Factory

Hackathon rules require a **runtime call** to Nebius Token Factory or Nebius AI Cloud plus an **NVIDIA open source model**. Tavily alone is not enough for Grand, Track, or Best Use of Tavily eligibility.

Nebius billing registration does not list Nigeria today. Do not use a false country. Use the paths below.

## Try before Discord

1. Sign in to [Token Factory](https://docs.tokenfactory.nebius.com/api-reference/introduction) with the same email as Devpost and Builders.
2. Open **balance → Top up → Apply promo code** only. Promo redemption does not require a bank card per Nebius docs.
3. If the product never asks for country until you pay with a card, you may still create **API keys** with a positive promo balance.
4. Watch the separate email for **$25 Token Factory credit** from the Builder Program and redeem every code on the same account.

If any step hard blocks on country before you can apply a promo or create a key, stop and use Discord.

## Discord (hackathon team)

Support pointed to hackathon specific help on Discord (see [Devpost Resources](https://nebiusglobalaihackathon.devpost.com/resources)).

Post in the hackathon channel:

```text
Hi, I am registered for the Nebius x NVIDIA Global AI Hackathon (Devpost). I am in Nigeria. Nebius billing registration does not offer Nigeria and support confirmed no manual exceptions for billing country. I have Builder Program and Devpost promo credits but cannot complete billing setup. What is the official path for hackathon participants to use Token Factory and Nemotron for a compliant submission? Project: GroundTruth (coding agent, Tavily + Nemotron). Thank you.
```

## While waiting

Keep building Tavily and agent tooling. Nemotron client stays behind `NEBIUS_API_KEY`. Do not submit until a judge can reproduce a live Nemotron call on Token Factory.

## LangSmith

LangChain credits may require a card on file to view balance. LangSmith is optional for this project. Skip unless you already use it for traces.

## Vercel `NEBIUS_API_KEY`

Use only the Token Factory **API key** string from the dashboard. Do not paste `Bearer ` in front. If you see `401 double authenticate`, delete the variable, create a new API key, redeploy, or leave empty until billing works (the app falls back on the sample demo).

## Tavily

Sign in at the Tavily dashboard with the same email as the redemption mail. Copy a `tvly-` API key into `.env` for demo hosting. Local dev can keep `tvly login` OAuth.
