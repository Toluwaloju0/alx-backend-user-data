#!/usr/bin/env python3
"""A module to create a new class to get and store instances from database"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """The class to get the user instance from the database"""

    def __init__(self):
        """The class initializer"""

        super()

    def create_session(self, user_id=None):
        """ To create and store the user_id"""

        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user = UserSession(user_id=user_id, session_id=session_id)
        self.user_id_by_session_id[session_id] = user
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """To get the user+id from a session"""

        user_session = self.user_id_by_session_id.get(session_id)

        if user_session is None:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """To destroy a user session when logout"""

        session_id = request.cookie.get('_my_session_id')
    
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user = UserSession.get(user_id)
        if user:
            user.remove()
