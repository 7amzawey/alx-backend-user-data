#!/usr/bin/env python3
"""Module for implementing a hashed_password."""
import bcrypt  # type: ignore


def hash_password(password: str) -> bytes:
    """Hash a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
