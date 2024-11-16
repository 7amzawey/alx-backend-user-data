#!/usr/bin/env python3
"""Module for session_auth a new authentication mechanism."""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """New mechanism for authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the a User id based on a session Id."""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a user instance."""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session/logout."""
        if request is None:
            return False
        if self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id
        return True
