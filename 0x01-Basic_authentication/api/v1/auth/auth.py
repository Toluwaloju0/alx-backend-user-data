#!/usr/bin/env python3
"""A module to create the Auth class"""

from flask import request
from typing import TypeVar, List


class Auth:
    """The class to implement the authentication system"""

    def __init__(self):
        """To initialize the class"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function to check if a path require authentication"""

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """To use the authorization header"""

        if request is None:
            return None
        return request.authorization

    def current_user(self, request=None) -> TypeVar('User'):
        """To get the current user"""

        return None
