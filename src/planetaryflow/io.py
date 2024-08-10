import cv2


def get_capture_metadata(capture: cv2.VideoCapture):
    return {
        "frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "fps": int(capture.get(5)),
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
