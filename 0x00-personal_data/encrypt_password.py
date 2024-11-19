#!/usr/bin/env python3
"""Module for implementing a hashed_password."""
import bcrypt  # type: ignore


def hash_password(password: str) -> bytes:
    """Hash a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the hashed_password is the actual password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
