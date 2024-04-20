import click
import cv2
from .segment import Segment

HELP_TEXT = "Planetary Flow v0.1.0"


@click.group(help=HELP_TEXT)
def cli() -> None:
    """Container object for the app"""
    click.echo("<CLI Root> beep boop")


@cli.command()
@click.option(
    "-d",
    default=None,
    help="Directory with files to process - can also be a single video file.",
)
def process(d):
    """Main processing pipeline"""
    click.echo(f"Directory {d}!")


# INTROSPECTION OPTIONS


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def segment(f):
    """Main processing pipeline"""
    click.echo(f"File {f}!")
    img = cv2.imread(f)
    s = Segment(img)
    cv2.imshow("Segmentation", s.mask.astype("uint8"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cli()
