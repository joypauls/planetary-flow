"""This is largely a dev utility for now, but it will be the primary entry point for the app."""

import click
import cv2
from .segmentation import Segmentation
from .alignment import global_translation
from .player import Player
from .utils import is_supported_image, is_supported_video

HELP_TEXT = "Planetary Flow v0.1.0"


##########################
# Primary User Interface #
##########################


@click.group(help=HELP_TEXT)
def cli() -> None:
    """Container object for the app"""
    click.echo("<CLI Root> beep boop")


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def play(f):
    """Play a video file"""
    click.echo(f"File {f}!")
    p = Player(file=f)
    p.play()


# @cli.command()
# @click.option(
#     "-d",
#     default=None,
#     help="Directory with files to process - can also be a single video file.",
# )
# def process(d):
#     """Main processing pipeline"""
#     click.echo(f"Directory {d}!")


####################################
# Introspection and Advanced Usage #
####################################


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def segment(f):
    """Examine object segmentation algorithm"""
    click.echo(f"Processing file: {f}")

    def build_segmentation_visual(img: cv2.UMat) -> cv2.UMat:
        s = Segmentation(img)
        # create a mask w/ green=object and red=background
        color_mask = cv2.cvtColor(s.mask, cv2.COLOR_GRAY2BGR)
        color_mask[:, :, 0][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask < 255] = 255
        # blend mask and original
        alpha = 0.15
        return cv2.addWeighted(img, 1 - alpha, color_mask, alpha, 0)

    if is_supported_image(f):
        img = cv2.imread(f)
        cv2.imshow("Segmentation", build_segmentation_visual(img))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif is_supported_video(f):
        p = Player(file=f, filter=build_segmentation_visual)
        p.play()
    else:
        raise ValueError("Unsupported file type")


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def stabilize(f):
    """Stabilization pipeline"""
    click.echo(f"Processing file: {f}")

    def build_stabilization_visual(img: cv2.UMat) -> cv2.UMat:
        img = global_translation(img, Segmentation(img))
        s = Segmentation(img)
        # create a mask w/ green=object and red=background
        color_mask = cv2.cvtColor(s.mask, cv2.COLOR_GRAY2BGR)
        color_mask[:, :, 0][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask < 255] = 255
        # blend mask and original
        alpha = 0.15
        return cv2.addWeighted(img, 1 - alpha, color_mask, alpha, 0)
        # return img

    if is_supported_image(f):
        img = cv2.imread(f)
        cv2.imshow("Segmentation", build_stabilization_visual(img))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif is_supported_video(f):
        p = Player(file=f, filter=build_stabilization_visual)
        p.play()
    else:
        raise ValueError("Unsupported file type")


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def quality(f):
    """Quality pipeline"""
    click.echo(f"Processing file: {f}")

    def build_quality_visual(img: cv2.UMat) -> cv2.UMat:
        img = global_translation(img, Segmentation(img))
        s = Segmentation(img)
        # create a mask w/ green=object and red=background
        color_mask = cv2.cvtColor(s.mask, cv2.COLOR_GRAY2BGR)
        color_mask[:, :, 0][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask == 255] = 0
        color_mask[:, :, 2][s.mask < 255] = 255
        # blend mask and original
        # alpha = 0.15
        # return cv2.addWeighted(img, 1 - alpha, color_mask, alpha, 0)
        return img

    if is_supported_image(f):
        img = cv2.imread(f)
        cv2.imshow("Segmentation", build_quality_visual(img))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif is_supported_video(f):
        p = Player(file=f, filter=build_quality_visual)
        p.play()
    else:
        raise ValueError("Unsupported file type")


#########################
# Dummy Command for Dev #
#########################


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def puppet(f):
    """Puppet pipeline"""
    click.echo(f"Processing file: {f}")

    def build_visual(img: cv2.UMat) -> cv2.UMat:
        # can we eliminate the double Segmention() call? or do we always need to resegment?
        img = global_translation(img, Segmentation(img))

        # # create a mask w/ green=object and red=background
        # s = Segmentation(img)
        # color_mask = cv2.cvtColor(s.mask, cv2.COLOR_GRAY2BGR)
        # color_mask[:, :, 0][s.mask == 255] = 0
        # color_mask[:, :, 2][s.mask == 255] = 0
        # color_mask[:, :, 2][s.mask < 255] = 255

        # blend mask and original
        # alpha = 0.15
        # return cv2.addWeighted(img, 1 - alpha, color_mask, alpha, 0)
        img = cv2.flip(cv2.rotate(img[150:650, 250:750], cv2.ROTATE_90_CLOCKWISE), 1)
        return img

    if is_supported_image(f):
        img = cv2.imread(f)
        cv2.imshow("Segmentation", build_visual(img))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif is_supported_video(f):
        p = Player(file=f, filter=build_visual)
        # p.write("./output/jupiter_globally_aligned.mp4", 20, 200, (500, 500))
        # p.write("./output/jupiter_seeing_illustration.mp4", 10, 100, (500, 500))
        p.play()
    else:
        raise ValueError("Unsupported file type")
