import numpy as np
import cv2

SHRINK_FACTOR = 0.75


class Threshold:
    """
    Segment image based on Otsu's method
    """

    def __init__(self, image):
        # TODO force uint8?
        self.gray = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
        if self.gray.dtype != np.uint8:
            raise TypeError("Not uint8, something's up")
        self._fit(self.gray)

    def _fit(self, img: np.ndarray):
        self.value, self.mask = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # this is to account for bias in data leading to aggressive threshold
        self.value = np.clip(int(self.value * SHRINK_FACTOR), 0, 255)

    def manual(self, threshold: int):
        """Manually override threshold"""
        self.value = np.clip(threshold, 0, 255)
        _, self.mask = cv2.threshold(self.gray, threshold, 255, cv2.THRESH_BINARY)

    def object_size(self):
        """Number of pixels in foreground mask"""
        return np.sum(self.mask == 255)
