# Judging alignment

Every track uses the same four criteria. GroundTruth is designed to score on all four, not only on Nebius and Nemotron depth.

## 01 Technological implementation

**Question:** How well is it built, and how effectively does it use Nebius and NVIDIA Nemotron?

**What judges should see**

| Proof | Where in the project |
|--------|----------------------|
| Runtime calls to Token Factory | `src/groundtruth/nemotron/client.py`, run logs in `data/runs/` |
| Multiple Nemotron tiers with purpose | Nano classify, Super patch, Ultra high risk in router + README table |
| Tavily at runtime | Research and Search in `src/groundtruth/tavily/` |
| Tests that pass after agent run | `fixtures/sample_project` golden path |
| Reproducible setup | README quick start |

**Submission copy:** Name exact model IDs, base URL, and one screenshot of playground vs app parity.

## 02 Design

**Question:** Is it a complete, coherent product experience, not just a technical proof of concept?

**What judges should see**

| Proof | Where in the project |
|--------|----------------------|
| Branded UI (Nebius lime, black, navy) | `apps/web`, `assets/brand/colors.css` |
| Clear layout: task, log, citations | Web dashboard, not raw JSON only |
| Empty and error states | UI copy when API or keys missing |
| Demo URL or polished CLI recording | Devpost link |

**Submission copy:** One sentence on who opens the app and what they do in the first 30 seconds.

## 03 Potential impact

**Question:** Does it make a credible, specific case for solving a real problem for a real audience?

**What judges should see**

| Proof | Where in the project |
|--------|----------------------|
| Specific audience | Maintainers, small teams, hackathon builders shipping on fast moving APIs |
| Specific pain | Hallucinated fixes when docs and releases drift |
| Measurable outcome | Tests green, citations attached, fewer bad merges |

**Submission copy:** Avoid “everyone needs AI.” Use “Python teams whose CI fails on dependency drift” or similar.

## 04 Quality of the idea

**Question:** Is it a creative, non obvious use of the platform, with real understanding of the problem?

**What judges should see**

| Proof | Where in the project |
|--------|----------------------|
| Non obvious twist | Evidence gate before patch, not chat then hope |
| Platform native | Nemotron routing for cost, Tavily Research schema, Token Factory as sole LLM |
| Understanding | Feedback docs with honest friction, not marketing |

**Submission copy:** Contrast with “Copilot that searches once.” GroundTruth blocks high risk edits without EvidencePack.

## Devpost feedback section

Complete all sponsor feedback fields. Point to `docs/nebius_feedback.md` and `docs/tavily_feedback.md` with real repro steps for Most Valuable Feedback.

## While keys are pending

Implement agent loop, UI, and fixtures with mocked evidence. Swap mocks for live clients in one commit when keys arrive. Judges care about runtime integration in the submitted demo, not draft history.
