#!/usr/bin/env python3
"""building an auth class mate."""
import bcrypt  # type: ignore


def _hash_password(password: str) -> bytes:
    """Return the hashed_password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
