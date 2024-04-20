"""Miscellaneous utilities"""

import os
from .constants import SUPPPORTED_IMAGE_FILE_TYPES, SUPPPORTED_VIDEO_FILE_TYPES


def is_supported_image(path: str) -> bool:
    _, file_extension = os.path.splitext(path)
    return file_extension.lower() in SUPPPORTED_IMAGE_FILE_TYPES


def is_supported_video(path: str) -> bool:
    _, file_extension = os.path.splitext(path)
    return file_extension.lower() in SUPPPORTED_VIDEO_FILE_TYPES
