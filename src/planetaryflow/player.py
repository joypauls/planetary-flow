"""
Render a video file with opencvsince there is no built-in
video player for my AVI's on a mac
Can be run standalone, or imported

TODO:
- support more than mp4
"""

import cv2
import numpy as np
from typing import Optional, Callable
from .constants import DEFAULT_FPS, CODECS


class Player:
    """
    Plays a video file filtered by a function, optionally saves result
    Filtering should NOT change dimensions of the frame (but might still play if it does)
    """

    def __init__(
        self,
        file: Optional[str] = None,
        # dir: Optional[str] = None,
        filter: Optional[Callable] = None,
        filter_debug: Optional[Callable] = None,
        n: float = np.inf,
    ):
        # check
        if not file:
            raise Exception("No file selected or passed in as an arg")
        # from args
        self.file = file
        # self.dir = dir
        self.n = n
        self.filter = filter
        self.filter_debug = filter_debug if filter_debug else None

        # main video
        self.capture = cv2.VideoCapture(file)
        self.capture_metadata = self._get_capture_metadata(self.capture)
        self.output = None

    def _get_capture_metadata(self, capture: cv2.VideoCapture):
        return {
            "frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
            "fps": capture.get(5),
            "width": capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            "height": capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
        }

    def _imshow_named(self, img: np.ndarray, name: str, x: int = 0, y: int = 0):
        # create a window and move
        cv2.namedWindow(name)
        cv2.moveWindow(name, x, y)
        cv2.imshow(name, img)

    def play(self, save_file: Optional[str] = None):
        """actual render loop"""
        if not self.file:
            raise Exception("No file selected or passed in as an arg")
        if save_file:
            self.output = cv2.VideoWriter(
                save_file,
                CODECS["mp4"],
                self.fps if self.fps else DEFAULT_FPS,
                (self.width, self.height),
            )
        title = f"Playing {self.file}" if self.file else "player.py"
        count = 0
        while self.capture.isOpened() and count < self.n:
            is_good, raw_frame = self.capture.read()
            if is_good:
                # show main window
                # conditionally apply filter for raw frame
                frame = self.filter(raw_frame) if self.filter else raw_frame

                # font = cv2.FONT_HERSHEY_SIMPLEX
                # text = "Frame Metrics\n{}x{}".format(
                #     self.capture_metadata["height"], self.capture_metadata["width"]
                # )
                # org = (
                #     10,
                #     20,
                # )  # Coordinates of the bottom-left corner of the text string in the image
                # fontScale = 0.5
                # color = (0, 255, 0)  # Blue color in BGR
                # thickness = 1
                # cv2.putText(
                #     frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA
                # )

                cv2.imshow(title, frame)
                self.output.write(frame) if self.output else None

                # handle user actions
                key = cv2.waitKey(20)
                # key = cv2.waitKey(0) & 0xFF
                if key == ord("q"):
                    # q or esc -> quit
                    break
                elif key == ord("p"):
                    # p or spacebar -> pause
                    cv2.waitKey(-1)
                elif key == ord("d"):
                    count += 1
                    # if count >= total_frames:
                    #     count = total_frames - 1
                    # cv2.waitKey(-1)
                elif key == ord("a"):
                    count -= 1
                    if count < 0:
                        count = 0
                    # cv2.waitKey(-1)
                else:
                    count += 1
            else:
                break
        self.close()

    def close(self):
        """close the video file"""
        self.capture.release()
        cv2.destroyAllWindows()


# if __name__ == "__main__":
#     args = _parse()
#     p = Player(file=args.file, dir=args.dir, n=args.n)
#     p.play()
