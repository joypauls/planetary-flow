import cv2
from enum import Enum


DEFAULT_FPS = 30
CODECS = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}


# colors for opencv visuals
class ColorsCV(Enum):
    RED = (0, 0, 255)
    GREEN = (0, 200, 0)
    BLUE = (255, 0, 0)
