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
