import pygments
import pygments.formatters
import pygments.formatters.terminal
import pygments.lexers
import pygments.token

pygments.formatters.terminal.TERMINAL_COLORS[pygments.token.Keyword] = (
    "magenta",
    "_",
)
pygments.formatters.terminal.TERMINAL_COLORS[pygments.token.String] = (
    "green",
    "_",
)
pygments.formatters.terminal.TERMINAL_COLORS[pygments.token.Number] = (
    "yellow",
    "_",
)
pygments.formatters.terminal.TERMINAL_COLORS[pygments.token.Punctuation] = (
    "brightblack",
    "_",
)


def colorize_sql(query: str) -> str:
    pretty_sql = pygments.highlight(
        query,
        pygments.lexers.PostgresLexer(),  # noqa
        pygments.formatters.TerminalFormatter(bg="light"),  # noqa
    )
    return pretty_sql
