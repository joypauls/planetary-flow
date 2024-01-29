"""Smoke tests mainly for development"""
# import numpy as np
import cv2
from planetaryflow.segment import Segment

jupiter = cv2.imread("./test/data/images/jupiter_stacked.png")


def test_segment():
    """Segment class smoke test"""

    # auto threshold
    s = Segment(jupiter)
    assert s.threshold > 0 & s.threshold < 255
    assert s.object_size() > 50

    # manual threshold
    s = Segment(jupiter, threshold=100)
    assert s.threshold == 100
    s.manual(-1)
    assert s.threshold == 0
    s.manual(256)
    assert s.threshold == 255

    # centroid sanity check
    s = Segment(jupiter)
    c = s.object_centroid()
    assert c[0] > 0 & c[0] < jupiter.shape[1]
    assert c[1] > 0 & c[1] < jupiter.shape[0]
    assert s.mask[c[1], c[0]] == 255
