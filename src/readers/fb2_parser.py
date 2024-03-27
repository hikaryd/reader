from .book_parser import BookParser


class Fb2Reader(BookParser):
    def parse(self, path): ...
