from .db.manager import DatabaseManager


def main():
    db_manager = DatabaseManager()
    db_manager.create_tables()


# EPUBBookParser().parse('book.epub')


if __name__ == '__main__':
    main()
