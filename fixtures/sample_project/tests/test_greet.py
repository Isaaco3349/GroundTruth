from sampledemo import greet


def test_greet_uses_groundtruth_brand():
    assert greet("builder") == "Hello builder from GroundTruth"
