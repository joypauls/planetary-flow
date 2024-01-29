import numpy as np
import cv2

SHRINK_FACTOR = 0.75


class Segment:
    """
    Segment image using a global threshold. Defaults to a modified Otsu's method.
    Produces a binary mask of the foreground to represent the object.
    """

    def __init__(
        self,
        image: np.ndarray,
        threshold: int = None,
    ):
        # TODO force uint8?
        self.gray = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
        if self.gray.dtype != np.uint8:
            raise TypeError("Not uint8, something's up")

        self.manual(threshold) if threshold else self._fit()

    def _fit(self):
        self.threshold, self.mask = cv2.threshold(
            self.gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # this is to account for bias in data leading to aggressive threshold
        self.threshold = np.clip(int(self.threshold * SHRINK_FACTOR), 0, 255)

    def manual(self, threshold: int):
        """Manually override threshold"""
        self.threshold = np.clip(threshold, 0, 255)
        _, self.mask = cv2.threshold(self.gray, threshold, 255, cv2.THRESH_BINARY)

    def object_size(self):
        """Number of pixels in object mask"""
        return np.sum(self.mask == 255)

    def object_centroid(self):
        """Centroid of object mask"""
        moments = cv2.moments(self.mask)
        return (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"]),
        )
