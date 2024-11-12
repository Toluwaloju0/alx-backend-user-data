#!/usr/bin/env python3
"""A module to log data to the stdout"""

import re


def filter_datum(fields, redaction, message, separator) -> str:
    """A function to log data ahich has hidden parts"""
    message = message.split(separator)
    for field in fields:
        re.sub(, f'{field}={redaction}', message)
    return message