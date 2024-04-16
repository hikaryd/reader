from textual.app import App, ComposeResult
from textual.widgets import Header

from components.footer import ReaderFooter


class Reader(App):
    TITLE = 'Terminal book reader'
    SUB_TITLE = 'Read books in the terminal'

    def compose(self) -> ComposeResult:
        yield Header()
        yield ReaderFooter()


if __name__ == '__main__':
    app = Reader()
    app.run()