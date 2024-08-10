from click.testing import CliRunner
from planetaryflow.cli import cli


###############
# Smoke Tests #
###############


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Planetary Flow" in result.output
