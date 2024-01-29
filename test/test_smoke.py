"""Smoke tests mainly for development"""

import numpy as np
import cv2

from planetaryflow.threshold import Threshold

jupiter = cv2.imread("./test/data/images/jupiter_stacked.png")


def test_threshold():
    """Threshold class smoke test"""

    # auto method
    t = Threshold(jupiter)
    assert t.value > 0 & t.value < 255
    assert t.object_size() > 50

    # manual method
    t = Threshold(jupiter)
    t.manual(100)
    assert t.value == 100
