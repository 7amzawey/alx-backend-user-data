#!/usr/bin/env python3
"""Auth class module."""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manange the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return false."""
        if (excluded_paths is None):
            return True
        if path is None:
            return True

        normalized_path = path.rstrip('/')
        normalized_excluded_paths = [p.rstrip('/') for p in excluded_paths]

        for excluded_path in normalized_excluded_paths:
            if excluded_path.endswith('*'):
                if normalized_path.startswith(excluded_path[:-1]):
                    return False
            elif normalized_path in normalized_excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return None."""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None."""
        return None
