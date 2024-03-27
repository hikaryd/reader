import os
import sqlite3


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.db_path = os.path.join(os.getcwd(), '.reader.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    @classmethod
    def create_tables(cls):
        books_table_query = """
        CREATE TABLE IF NOT EXISTS Books (
            BookID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Author TEXT,
            Genre TEXT,
            Year INTEGER,
            Format TEXT NOT NULL,
            Path TEXT NOT NULL
        );
        """

        pages_table_query = """
        CREATE TABLE IF NOT EXISTS Pages (
            PageID INTEGER PRIMARY KEY AUTOINCREMENT,
            BookID INTEGER,
            PageNumber INTEGER NOT NULL,
            Content TEXT NOT NULL,
            FOREIGN KEY (BookID) REFERENCES Books(BookID)
        );
        """

        instance = cls()
        instance.cursor.execute(books_table_query)
        instance.cursor.execute(pages_table_query)
        instance.conn.commit()

    def close(self):
        self.conn.close()

    @classmethod
    def add_book(cls, title, author, genre, year, format, path):
        instance = cls()
        instance.cursor.execute(
            'INSERT INTO Books (Title, Author, Genre, Year, Format, Path) VALUES (?, ?, ?, ?, ?, ?)',
            (title, author, genre, year, format, path),
        )
        instance.conn.commit()
        return instance.cursor.lastrowid

    @classmethod
    def add_page(cls, book_id, page_number, content):
        instance = cls()
        instance.cursor.execute(
            'INSERT INTO Pages (BookID, PageNumber, Content) VALUES (?, ?, ?)',
            (book_id, page_number, content),
        )
        instance.conn.commit()

    @classmethod
    def update_book(
        cls,
        book_id,
        title,
        author,
        genre,
        year,
        format,
    ):
        instance = cls()
        instance.cursor.execute(
            'UPDATE Books SET Title = ?, Author = ?, Genre = ?, Year = ?, Format = ? WHERE BookID = ?',
            (title, author, genre, year, format, book_id),
        )
        instance.conn.commit()

    @classmethod
    def get_book_id_by_path(cls, path):
        instance = cls()
        instance.cursor.execute('SELECT BookID FROM Books WHERE Path = ?', (path,))
        row = instance.cursor.fetchone()
        return row[0] if row else None

    @classmethod
    def delete_pages_by_book_id(cls, book_id):
        instance = cls()
        instance.cursor.execute('DELETE FROM Pages WHERE BookID = ?', (book_id,))
        instance.conn.commit()
