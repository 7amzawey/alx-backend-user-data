#!/usr/bin/env python3
"""Module for a logger function."""
import re
import logging
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """Return loggin.Logger."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formattter = logging.ReactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formattter)
    logger.addHandler(stream_handler)


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Return a log message obfuscated."""
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redact Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init method."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the logging Record."""
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            self.REDACTION, original_message, self.SEPARATOR)
