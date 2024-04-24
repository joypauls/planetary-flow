import numpy as np
import cv2


class Segmentation:
    """
    Segment img using a global threshold. Defaults to a modified Otsu's method.
    Produces a binary mask of the foreground to represent the object.
    """

    # compensates for overly aggressive thresholding
    SHRINK_FACTOR = 0.75

    def __init__(
        self,
        img: np.ndarray,
        threshold: int = None,
    ):
        # convert to grayscale
        # TODO force uint8?
        # TODO configurable denoising
        self.gray = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
        if self.gray.dtype != np.uint8:
            raise TypeError("Not uint8, something's up")

        self.threshold = threshold
        self.mask = None
        self.manual(threshold) if threshold else self._fit()

    def _fit(self):
        self.threshold, _ = cv2.threshold(
            self.gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        # this is to account for bias in data leading to aggressive threshold
        self.threshold = np.clip(
            int(self.threshold * Segmentation.SHRINK_FACTOR), 0, 255
        )
        # create binary mask
        self.mask = self.gray.copy()
        self.mask[self.mask > self.threshold] = 255

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
