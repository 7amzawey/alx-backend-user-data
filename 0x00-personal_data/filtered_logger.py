#!/usr/bin/env python3
"""Module for a logger function."""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Return a log message obfuscated."""
    escaped_fields = [re.escape(word) for word in fields]
    pattern = r'(' + '|'.join(f"{word}=" for word in escaped_fields) + r')([^' + re.escape(separator) + r']+)'
    return re.sub(pattern, lambda m: m.group(1) + redaction, message)
