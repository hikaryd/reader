from textual.widget import Text
from textual.widget import Widget, RenderableType
from textual.widgets import Header
from textual.reactive import Reactive


class HeaderTitle(Widget):
    DEFAULT_CSS = '''
    HeaderTitle {
        content-align: center middle;
        width: 100%;
    }
    '''
    title = Reactive[str]('Book reader')
    progress = Reactive[str]('')

    def render(self) -> RenderableType:
        text = Text(self.title, no_wrap=True, overflow='ellipsis')
        if self.progress:
            text.append(' - ')
            text.append(self.progress)
        return text


class ReaderHeader(Header):
    def compose(self):
        yield HeaderTitle()
