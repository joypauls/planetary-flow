from click.testing import CliRunner
from app import hello


def test_hello():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice!" in result.output


def test_hello_prompt():
    runner = CliRunner()
    result = runner.invoke(hello, input="Alice\n")
    assert result.exit_code == 0
    assert "Hello Alice!" in result.output
