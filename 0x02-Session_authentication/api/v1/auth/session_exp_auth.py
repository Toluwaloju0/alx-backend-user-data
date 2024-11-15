#!/usr/bin/env python3
""" A module to create a class for authentication expiration"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class to make a session exp"""

    def __init__(self):
        """ Th initializing of the class"""

        super().__init__()
        str_duration = getenv('SESSION_DURATION')
        if str_duration is None or str_duration.isdigit() is False:
            self.session_duration = 0
        else:
            self.session_duration = int(str_duration)

    def create_session(self, user_id=None):
        """A method to create a session from the super class"""

        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ a method to get a user_id from the session id"""
        if (
            session_id is None
            or self.user_id_by_session_id.get(session_id) is None
            or self.user_id_by_session_id[session_id].get('created_at') is None
            or self.user_id_by_session_id[session_id].get(
                'created_at'
            ) + timedelta(seconds) < datetime.now()
            or self.session_durtion > 0
        ):
            return None
        return self.user_id_by_session_id.get(session_id)
