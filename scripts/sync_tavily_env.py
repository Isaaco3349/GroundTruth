"""Copy Tavily credentials from CLI config into project .env (no stdout secrets)."""

from __future__ import annotations

import re
from pathlib import Path

from tavily_cli.config import get_api_key

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
EXAMPLE = ROOT / ".env.example"


def main() -> int:
    key = get_api_key()
    if not key:
        print("No Tavily credential found. Run tvly login first.")
        return 1

    if not key.startswith("tvly-"):
        print(
            "CLI OAuth is active. GroundTruth will read credentials from tvly config at runtime. "
            "Optional: add a tvly API key from the Tavily dashboard to .env for deployments."
        )
        return 0

    if not ENV_PATH.exists() and EXAMPLE.exists():
        ENV_PATH.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")

    text = ENV_PATH.read_text(encoding="utf-8") if ENV_PATH.exists() else ""
    line = f"TAVILY_API_KEY={key}\n"
    if re.search(r"^TAVILY_API_KEY=.*$", text, flags=re.MULTILINE):
        text = re.sub(r"^TAVILY_API_KEY=.*$", line.strip(), text, flags=re.MULTILINE)
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        text += line

    ENV_PATH.write_text(text, encoding="utf-8")
    print("Updated .env with Tavily credential from CLI config.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
