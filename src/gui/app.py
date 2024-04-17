from textual.app import App, ComposeResult

from components.footer import ReaderFooter
from components.header import ReaderHeader


class Reader(App):

    COMMANDS = {}

    def compose(self) -> ComposeResult:
        yield ReaderHeader()
        yield ReaderFooter()


if __name__ == '__main__':
    app = Reader()
    app.run()