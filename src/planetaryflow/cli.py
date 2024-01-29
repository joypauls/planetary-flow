import click


@click.command()
def cli() -> None:
    print("Planetary Flow")


if __name__ == "__main__":
    cli()
