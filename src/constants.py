import cv2
from enum import Enum


# colors for opencv visuals
class Colors(Enum):
    RED = (0, 0, 255)
    GREEN = (0, 200, 0)
    BLUE = (255, 0, 0)


CODECS = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}
