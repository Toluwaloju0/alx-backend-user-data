#!/usr/bin/env python3
"""A module to create the session auth"""

from api.v1.auth.auth import Auth
from models.user import User
from os import getenv
from uuid import uuid4


class SessionAuth(Auth):
    """Thr class for the session Auth method"""

    user_id_by_session_id = {}

    def __init__(self):
        """The init class"""

        super()

    def create_session(self, user_id: str = None) -> str:
        """A method to create a session for the user"""

        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user_id baed on the session_id"""

        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ A function to get a user based on a cookie value"""

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if user_id is not None:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """ To destroy the session when logput"""

        session_id = self.session_cookie(request)
        if request is None or session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
