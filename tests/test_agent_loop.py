from groundtruth.agent.loop import run_task
from groundtruth.models import EvidenceClaim, EvidencePack, RunStatus, SourceCitation
from groundtruth.tavily import fetch as fetch_mod


def test_run_completes_with_mocked_tavily(monkeypatch):
    pack = EvidencePack(
        query="q",
        claims=[EvidenceClaim(id="1", text="Use correct return string in greet")],
        sources=[SourceCitation(url="https://docs.pytest.org", title="pytest")],
    )
    monkeypatch.setattr(fetch_mod, "load_evidence", lambda *a, **k: pack)

    record = run_task("Fix the failing test in the sample project", "test-run-id")
    assert record.status == RunStatus.completed
    assert record.evidence is not None
    assert "passed" in record.summary.lower()
