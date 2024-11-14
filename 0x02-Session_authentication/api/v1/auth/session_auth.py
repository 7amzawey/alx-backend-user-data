#!/usr/bin/env python3
"""Module for session_auth a new authentication mechanism."""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """New mechanism for authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID."""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id