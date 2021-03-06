from io import StringIO

from toxn.config.cli import build_parser
from toxn.evaluate import main


def test_help(capsys):
    code = main(['--help', '-v', 'WARNING'])
    assert code == 0

    out, err = capsys.readouterr()
    assert not err
    help_message_io = StringIO()
    build_parser().print_help(help_message_io)
    assert out == help_message_io.getvalue()
