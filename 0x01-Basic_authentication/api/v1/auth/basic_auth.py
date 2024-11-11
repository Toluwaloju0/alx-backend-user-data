#!/usr/bin/env python3
"""A module for the basic auth class"""

from api.v1.auth.auth import Auth


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
