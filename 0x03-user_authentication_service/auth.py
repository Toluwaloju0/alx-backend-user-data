#!/usr/bin/env python3
"""A module to hash a password"""

import uuid
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User


def _hash_password(password: str) -> bytes:
    """To hash a password"""

    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """A function to create a uuid"""

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """A method to register a new user"""

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ A method to check if the password for a user is correct"""

        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """A method to create a session id for a user"""

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> None:
        """To get a user from his session id"""

        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """To remove the session id of a user"""

        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """A method to create a user reset token uuid"""

        try:
            # get the user using DB.find_user_by
            user = self._db.find_user_by(email=email)
            reset_id = _generate_uuid()
            self._db.update(user.id, reset_token=reset_id)
            return reset_id

        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """A method to update the user password"""

        try:
            user = self.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id,
                hashed_password=_hash_password(password),
                reset_token=None
            )

            return None

        except (NoResultFound, InvalidRequestError):
            raise ValueError
