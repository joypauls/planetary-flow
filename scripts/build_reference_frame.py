import os
import cv2
import numpy as np
from planetaryflow.io import get_capture_metadata
from planetaryflow.segmentation import Segmentation

# starting point here is a globally aligned video
INPUT_VIDEO = "./output/jupiter_globally_aligned.avi"
capture = cv2.VideoCapture(INPUT_VIDEO)

print("----------")
print(f"working dir: {os.getcwd()}")
print(f"metadata: {get_capture_metadata(capture)}")


##################
# GLOBAL QUALITY #
##################


def rms_constrast(img):
    return img.std()


def michelson_constrast(img):
    minimum = np.min(img).astype(np.float32)
    maximum = np.max(img).astype(np.float32)
    return (maximum - minimum) / (maximum + minimum)


def contrast_metric(img):
    s = Segmentation(img)
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)[:, :, 0]
    lum = cv2.GaussianBlur(lum, (5, 5), 0)
    # lum[s.mask == 0] = 0
    # return rms_constrast(lum)
    return lum[s.mask == 255].std()


frame_indices = []
quality_values = []
frame_index = 0
while capture.isOpened():
    is_good, frame = capture.read()
    if is_good:
        value = contrast_metric(frame)
        frame_indices.append(frame_index)
        quality_values.append(value)
        frame_index += 1
    else:
        break
capture.release()

# re-sort based on quality values
sorted_indices = [idx for _, idx in sorted(zip(quality_values, frame_indices))]

# print(sorted(quality_values))
print("-----")
print(np.quantile(quality_values, [0, 0.25, 0.5, 0.75, 1]))
print("-----")
print(sorted_indices.index(0))

# capture = cv2.VideoCapture(INPUT_VIDEO)
# for sorted_index in sorted_indices:
#     capture.set(cv2.CAP_PROP_POS_FRAMES, sorted_index)
#     ret, frame = capture.read()
#     if not ret:
#         break
#     cv2.imshow("Reordered Video", frame)
#     if cv2.waitKey(30) & 0xFF == ord("q"):  # Press 'q' to quit
#         break
# capture.release()
# cv2.destroyAllWindows()


######################
# STACKING REFERENCE #
######################

# compute average image
capture = cv2.VideoCapture(INPUT_VIDEO)
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

# average_image = np.uint16(average_image)
cv2.imshow("Reordered Video", average_image.astype(np.uint8))

average_image = cv2.normalize(average_image, None, 0, 65535, cv2.NORM_MINMAX)
cv2.imwrite("./output/stacked_reference_frame.png", average_image.astype(np.uint16))
cv2.imwrite("./output/stacked_reference_frame.tiff", average_image.astype(np.uint16))
cv2.waitKey(0)
cv2.destroyAllWindows()


if __name__ == "__main__":
    pass
