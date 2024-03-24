import click
import cv2
from .segment import Segment

HELP_TEXT = "Planetary Flow v0.1.0"


@click.group(help=HELP_TEXT)
def cli() -> None:
    """Container object for the app"""
    click.echo("beep boop")


@cli.command()
@click.option(
    "-d",
    default=None,
    help="Directory with files to process - can also be a single video file.",
)
def process(dir):
    """Main processing pipeline"""
    click.echo(f"Directory {dir}!")


# INTROSPECTION OPTIONS


@cli.command()
@click.option(
    "-f",
    default=None,
    help="",
)
def segment(file):
    """Main processing pipeline"""
    click.echo(f"Directory {dir}!")
    img = cv2.imread(file)
    s = Segment(img)
    cv2.imshow("Mean Image", mean_image.astype("uint8"))


if __name__ == "__main__":
    cli()
