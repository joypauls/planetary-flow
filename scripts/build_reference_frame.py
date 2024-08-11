import os
import cv2
import numpy as np
from planetaryflow.io import get_capture_metadata

# starting point here is a globally aligned video
INPUT_VIDEO = "./output/jupiter_globally_aligned.mp4"
capture = cv2.VideoCapture(INPUT_VIDEO)

print("----------")
print(f"working dir: {os.getcwd()}")
print(f"metadata: {get_capture_metadata(capture)}")


##################
# GLOBAL QUALITY #
##################


######################
# STACKING REFERENCE #
######################

# compute average image
_, first_frame = capture.read()
average_image = first_frame.astype(np.float32)
count = 1
while capture.isOpened():
    is_good, frame = capture.read()
    if is_good:
        count += 1
    else:
        break
    average_image += frame.astype(np.float32)
capture.release()

average_image /= count

print(f"processed {count}")
print(f"average image shape: {average_image.shape}")
print(f"average image min: {average_image.min()}")
print(f"average image max: {average_image.max()}")
print(f"average image mean: {average_image.mean()}")

average_image = np.uint8(average_image)

if __name__ == "__main__":
    pass
