from pathlib import Path

from groundtruth.tools import workspace as ws

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "fixtures" / "sample_project"


def test_infer_expected_from_tests():
    expected = ws.infer_expected_from_tests(SAMPLE)
    assert expected == "Hello builder from GroundTruth"


def test_reset_and_pytest_cycle():
    ws.reset_sample_bug(SAMPLE)
    code, _ = ws.run_pytest(SAMPLE)
    assert code != 0


def test_verify_sample_greet_after_fix():
    ws.reset_sample_bug(SAMPLE)
    expected = ws.infer_expected_from_tests(SAMPLE)
    assert expected
    ws.write_text_file(
        SAMPLE,
        "sampledemo/__init__.py",
        f'def greet(name: str) -> str:\n    return "{expected}"\n',
    )
    code, out = ws.verify_sample_greet(SAMPLE)
    assert code == 0
    assert "passed" in out.lower()
