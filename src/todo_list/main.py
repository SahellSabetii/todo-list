from todo_list.cli.console import cli
from todo_list.db.session import db


if __name__ == '__main__':
    db.create_tables()
    cli()
