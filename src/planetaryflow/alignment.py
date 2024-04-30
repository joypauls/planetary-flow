import cv2
import numpy as np

from .segmentation import Segmentation


def global_translation(img: cv2.UMat, s: Segmentation) -> cv2.UMat:
    """Global translation"""
    m = cv2.moments(s.mask)
    centroid = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))
    height, width, _ = img.shape
    dx = int(width / 2) - centroid[0]
    dy = int(height / 2) - centroid[1]

    # transformation in homogeneous form
    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])

    return cv2.warpAffine(img, translation_matrix, (img.shape[1], img.shape[0]))
