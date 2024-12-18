#!/usr/bin/env python3
"""Building an auth class mate."""
import bcrypt  # type: ignore
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Return the hashed_password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a string representation of the uuid module."""
    import uuid
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize method."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Return a User."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the password is valid."""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session and return its id."""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = str(uuid.uuid4())
            self._db._session.commit()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user form session_id."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id) -> None:
        """Update the user's session ID to None."""
        usr = self._db.find_user_by(id=user_id)
        usr.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Change the password."""
        try:
            usr = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(usr.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        new_hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_hashed_password)
        self._db.update_user(user.id, session_id=None)
        self._db._session.commit()
