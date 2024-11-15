#!/usr/bin/env bash
"""A new class to store user sessions in the database"""

from models.base import Base


class UserSession(Base):
    """The class to store the user sessions"""

    def __init__(self, *args: list, **kwargs: dict):
        """The initializer for the class"""

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
