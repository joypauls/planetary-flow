import cv2
from planetaryflow.io import get_capture_metadata

capture = cv2.VideoCapture("./tests/data/videos/jupiter.mp4")


def test_get_capture_metadata():
    print(get_capture_metadata(capture))
    metadata = get_capture_metadata(capture)
    assert metadata["frames"] == 500
