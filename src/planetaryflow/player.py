"""
Render a video file with opencvsince there is no built-in
video player for my AVI's on a mac
Can be run standalone, or imported

TODO:
- support more than mp4
"""

import cv2
import numpy as np
from typing import Optional, Callable, Tuple
from .constants import DEFAULT_FPS, CODECS


class Player:
    """
    Plays a video file filtered by a function, optionally saves result
    Filtering should NOT change dimensions of the frame (but might still play if it does)
    """

    def __init__(
        self,
        file: Optional[str] = None,
        filter: Optional[Callable] = None,
        n: float = np.inf,
    ):
        # handle bad calls
        if not file:
            raise Exception("No file selected or passed in as an arg")

        # fields from args
        self.file = file
        # self.n = n
        self.filter = filter

        # main video
        self.capture = cv2.VideoCapture(file)
        self.capture_metadata = self._get_capture_metadata(self.capture)
        self.output = None

        # state
        self.paused = False

    def _get_capture_metadata(self, capture: cv2.VideoCapture):
        return {
            "frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
            "fps": int(capture.get(5)),
            "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }

    # def _imshow_named(self, img: np.ndarray, name: str, x: int = 0, y: int = 0):
    #     # create a window and move
    #     cv2.namedWindow(name)
    #     cv2.moveWindow(name, x, y)
    #     cv2.imshow(name, img)

    def write(
        self,
        output_file: str,
        fps: int,
        n: int = np.inf,
        output_size: Optional[Tuple[int, int]] = None,
    ):
        """process frames and write to output file"""
        output_size = (
            output_size
            if output_size
            else (self.capture_metadata["width"], self.capture_metadata["height"])
        )
        out = cv2.VideoWriter(
            output_file, CODECS["mp4"], fps if fps else DEFAULT_FPS, output_size
        )
        count = 0
        while self.capture.isOpened() and count < n:
            is_good, raw_frame = self.capture.read()
            if is_good:
                # conditionally apply filter for raw frame
                out.write(self.filter(raw_frame) if self.filter else raw_frame)
                count += 1
            else:
                break

    def play(self, save_file: Optional[str] = None):
        """render loop"""
        # debugging
        print(self.capture_metadata)

        title = f"Playing {self.file}" if self.file else "player.py"
        count = 0
        while self.capture.isOpened():

            if not self.paused:
                is_good, raw_frame = self.capture.read()
                if is_good:
                    # show main window
                    # conditionally apply filter for raw frame
                    cv2.imshow(
                        title, self.filter(raw_frame) if self.filter else raw_frame
                    )
                    count += 1
                else:
                    break

            # handle user actions
            key = cv2.waitKey(33) & 0xFF
            # key = cv2.waitKey(0) & 0xFF
            if key == ord("q"):
                # q or esc -> quit
                break
            elif key == ord("p"):
                # p or spacebar -> pause
                self.paused = not self.paused
            elif self.paused:
                if key == ord("d"):
                    count += 1
                    # if count >= total_frames:
                    #     count = total_frames - 1
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, count)
                    is_good, raw_frame = self.capture.read()
                    if is_good:
                        cv2.imshow(
                            title,
                            self.filter(raw_frame) if self.filter else raw_frame,
                        )
                elif key == ord("a"):
                    count -= 1
                    if count < 0:
                        count = 0
                    self.capture.set(cv2.CAP_PROP_POS_FRAMES, count)
                    is_good, raw_frame = self.capture.read()
                    if is_good:
                        cv2.imshow(
                            title,
                            self.filter(raw_frame) if self.filter else raw_frame,
                        )

        self.close()

    def close(self):
        """close the video file"""
        self.capture.release()
        cv2.destroyAllWindows()


# if __name__ == "__main__":
#     args = _parse()
#     p = Player(file=args.file, dir=args.dir, n=args.n)
#     p.play()
