#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from typing import Iterable


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """To add a new user
        to the database"""

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, *args: Iterable, **kwargs: dict) -> User:
        """To  get a user
        using kwargs"""

        from sqlalchemy.orm.exc import NoResultFound
        from sqlalchemy.exc import InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except (InvalidRequestError, NoResultFound):
            raise

    def update_user(self, user_id: int, *args: Iterable, **kwargs: dict) -> None:
        """A method to update a user instance"""

        # list the allowed attributes
        attributes = [
            'id', 'email', 'hashed_password',
            'session_id', 'reset_token'
        ]

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key in attributes:
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()
        return None
