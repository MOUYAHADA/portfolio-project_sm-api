#!/usr/bin/env python3
"""
Module for utility functions
"""
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    """Hash a password"""
    if not password:
        raise ValueError("A password must be provided")
    encoded = password.encode("utf-8")
    hashed_password = hashpw(encoded, gensalt(12))
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a hashed password"""
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
