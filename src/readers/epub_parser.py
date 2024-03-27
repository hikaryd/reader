import re

from ebooklib import epub

from ..db.manager import DatabaseManager
from .book_parser import BookParser


class EPUBBookParser(BookParser):
    def parse(self, path):
        book = epub.read_epub(path)
        title = book.get_metadata('DC', 'title')[0][0]
        authors = ', '.join(
            [author[0] for author in book.get_metadata('DC', 'creator')]
        )
        year = (
            book.get_metadata('DC', 'date')[0][0][:4]
            if book.get_metadata('DC', 'date')
            else 'Unknown'
        )
        genre = (
            book.get_metadata('DC', 'subject')[0][0]
            if book.get_metadata('DC', 'subject')
            else 'Unknown'
        )

        book_id = DatabaseManager.get_book_id_by_path(path)
        if book_id is not None:
            DatabaseManager.update_book(
                book_id,
                title,
                authors,
                genre,
                year,
                'EPUB',
            )
        else:
            book_id = DatabaseManager.add_book(
                title,
                authors,
                genre,
                year,
                'EPUB',
                path,
            )

        self.save_pages(book, book_id)

    def save_pages(self, book, book_id):
        DatabaseManager.delete_pages_by_book_id(book_id)
        all_content = ''
        for item in book.get_items():
            if isinstance(item, epub.EpubHtml):
                content = item.get_body_content().decode('utf-8')  # type: ignore
                all_content += self.remove_html_tags(self.normalize_newlines(content))

        pages = self.split_into_pages(all_content)

        page_number = 1
        for content in pages:
            DatabaseManager.add_page(book_id, page_number, content)
            page_number += 1

    def remove_html_tags(self, text):
        return re.sub(r'<[^>]+>', '', text)
