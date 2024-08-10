"""Smoke tests mainly for development"""

# import numpy as np
import pytest
import cv2
from planetaryflow.segmentation import Segmentation

jupiter1 = cv2.imread("./tests/data/images/jupiter_stacked.png")
jupiter2 = cv2.imread("./tests/data/images/jupiter_frame_lowq.png")
moon = cv2.imread("./tests/data/images/moon_stacked_sharpened.jpg")
test_images = [jupiter1, jupiter2, moon]


@pytest.mark.parametrize("img", test_images)
def test_segmentation(img):
    """Segment class smoke tests"""

    # auto threshold
    s = Segmentation(img)
    assert s.threshold > 0 & s.threshold < 255
    assert s.object_size() > 50

    # manual threshold
    s = Segmentation(img, threshold=100)
    assert s.threshold == 100
    s.manual(-1)
    assert s.threshold == 0
    s.manual(256)
    assert s.threshold == 255

    # centroid sanity check
    s = Segmentation(img)
    c = s.object_centroid()
    assert c[0] > 0 & c[0] < img.shape[1]
    assert c[1] > 0 & c[1] < img.shape[0]
    assert s.mask[c[1], c[0]] == 255
