from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from todo_list.db.session import db


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Automatically closes the session after request is complete.
    """
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()
