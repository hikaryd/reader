import re
from abc import ABC, abstractmethod


class BookParser(ABC):
    @abstractmethod
    def parse(self, path):
        """Чтение книги из файла."""

    def split_into_pages(self, content: str, chars_per_page=1000):
        pages = []
        while content:
            if len(content) <= chars_per_page:
                pages.append(content)
                break

            page_break = content.rfind(' ', 0, chars_per_page)
            if page_break == -1:
                page_break = chars_per_page

            pages.append(content[:page_break])
            content = content[page_break:].lstrip()

        return pages

    def normalize_newlines(self, text):
        return re.sub(r'\n{2,}', '\n', text)
