import os
import cv2
import numpy as np
from planetaryflow.io import get_capture_metadata

# starting point here is a globally aligned video
INPUT_VIDEO = "./output/jupiter_globally_aligned.mp4"
capture = cv2.VideoCapture(INPUT_VIDEO)

if __name__ == "__main__":
    print("----------")
    print(f"working directory: {os.getcwd()}")
    print(get_capture_metadata(capture))
