from groundtruth.models import ModelTier
from groundtruth.nemotron.router import choose_tier


def test_ultra_for_architecture():
    assert choose_tier("Plan a large architecture refactor") == ModelTier.ultra


def test_super_for_fix():
    assert choose_tier("Fix the failing test") == ModelTier.super
