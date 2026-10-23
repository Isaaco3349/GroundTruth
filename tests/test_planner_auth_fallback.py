from pathlib import Path

from groundtruth.agent import planner
from groundtruth.models import EvidencePack
from groundtruth.nemotron.client import NemotronClient


class BrokenNemotron(NemotronClient):
    def is_configured(self) -> bool:
        return True

    def complete(self, tier, system, user):
        raise RuntimeError('Error code: 401 - {"message": "double authenticate"}')


def test_plan_patch_falls_back_on_401(tmp_path, monkeypatch):
    workspace = tmp_path
    (workspace / "tests").mkdir()
    (workspace / "tests" / "test_greet.py").write_text(
        'from sampledemo import greet\n'
        'def test_x():\n'
        '    assert greet("builder") == "Hello builder from GroundTruth"\n',
        encoding="utf-8",
    )
    (workspace / "sampledemo").mkdir()
    (workspace / "sampledemo" / "__init__.py").write_text(
        'def greet(name): return "x"\n', encoding="utf-8"
    )
    pack = EvidencePack(query="q")
    patch, tier = planner.plan_patch(
        workspace,
        "fix test",
        pack,
        {},
        client=BrokenNemotron(),
    )
    assert tier is None
    assert patch["relative_path"] == "sampledemo/__init__.py"
    assert "GroundTruth" in patch["content"]
