#!/usr/bin/env python3
"""A module for the basic auth class"""

from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """A class for the basic auth"""

    def __init__(self):
        """The initialize function"""

        super()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """To get the 64 encoded string from the header
        if it starts with Basic"""

        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None

        header_list = authorization_header.split()
        if header_list[0] == 'Basic':
            return header_list[1]
        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """A function to decode the 64base encoded
        string in the authorization header"""

        import base64

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """A function to retrun te authorization email and passwors"""

        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        string = decoded_base64_authorization_header.split(':')
        if type(string) is list and len(string) == 2:
            return string[0], string[1]
        return None, None

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """To get the user instance from the DB
        based on his email and password"""

        from models.user import User

        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        user_list = User.search({'email': user_email})
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
