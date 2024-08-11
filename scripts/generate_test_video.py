"""
Goal is to generate some small/short files from longer real data

Input: Raw (some cropped) video files

"""

import cv2

VIDEO_FILES = [
    "raw/2023-11-30-0112_6-Jupiter.AVI",
]
VIDEO_LABELS = ["jupiter"]
OFFSETS = [0, 0, 0]
N_FRAMES = 200
OUTPUT_FPS = 30
CODECS = {
    "avi": cv2.VideoWriter_fourcc(*"FFV1"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}

for i, path in enumerate(VIDEO_FILES):
    # open video
    try:
        vid_capture = cv2.VideoCapture(path)
        fps = vid_capture.get(5)
        print("Frames per second : ", fps, "FPS")
        frame_count = vid_capture.get(7)
        print("Frame count : ", frame_count)
    except Exception as e:
        print(f"Error reading {path}")
        print(e)

    # initialize video writer object
    output = cv2.VideoWriter(
        "output/" + VIDEO_LABELS[i] + ".avi",
        CODECS["avi"],
        OUTPUT_FPS,
        (1000, 800),
    )

    count = 0
    while vid_capture.isOpened() and count < N_FRAMES:
        is_good, frame = vid_capture.read()
        if is_good:
            # crop
            # this should be something configurable
            frame = frame[
                OFFSETS[i] : 800 + OFFSETS[i], 400 + OFFSETS[i] : 1400 + OFFSETS[i]
            ]
            # write the frame to the output file
            output.write(frame)
        else:
            break
        count += 1

    vid_capture.release()
    # Release the video capture object
    output.release()
