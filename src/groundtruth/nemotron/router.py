"""Nemotron tier routing. Implementation follows in the build phase."""

from groundtruth.models import ModelTier


def choose_tier(task: str, risk_high: bool = False) -> ModelTier:
    lowered = task.lower()
    if risk_high or any(k in lowered for k in ("architecture", "refactor", "migrate", "security")):
        return ModelTier.ultra
    if any(k in lowered for k in ("fix", "test", "lint", "typo", "import")):
        return ModelTier.super
    return ModelTier.nano
