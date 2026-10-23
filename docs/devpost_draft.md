# Devpost submission draft

Edit before paste into Devpost.

## Project name

GroundTruth

## Tagline

A coding agent that will not ship without cited web evidence, powered by Nemotron on Nebius Token Factory and Tavily Research.

## Track

Coding and Agentic Engineering

## What we built

GroundTruth reads a task against a local repository, gathers Tavily Research when the task depends on changing APIs or external facts, routes Nemotron Nano, Super, and Ultra on Nebius Token Factory, applies patches through audited tools, and runs tests until green. The web UI shows every claim next to its sources.

## Why we built it

Hallucinated API fixes waste time and credits. We wanted an agent that behaves like a careful engineer: research first, patch second, prove with tests.

## How we used Nebius and NVIDIA

- Token Factory OpenAI compatible endpoint for all inference
- Nemotron Nano for classification and routing
- Nemotron Super for code edits
- Nemotron Ultra for high risk planning (demo and edge cases)

## How we used Tavily

- Research API with structured EvidencePack schema
- Search advanced depth for official documentation
- Optional streaming in the UI during long research tasks

## Demo links

- Live app: TBD
- Video: TBD
- Repository: TBD

## Feedback

See `docs/nebius_feedback.md` and `docs/tavily_feedback.md` in the repository.
