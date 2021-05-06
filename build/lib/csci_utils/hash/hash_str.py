import base64
import os
import hashlib

from typing import Union
from canvasapi import Canvas
from environs import Env


def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """
    # Hint: use os.environment and bytes.fromhex
    return bytes.fromhex(os.environ["CSCI_SALT"])


def get_csci_pepper() -> bytes:
    """Returns the appropriate pepper for CSCI E-29

    This is similar to the salt, but defined as the UUID of the Canvas course,
    available from the Canvas API.

    This value should never be recorded or printed.

    :return: bytes representation of the pepper
    """

    # Hint: Use base64.b64decode to decode a UUID string to bytes
    env = Env()
    course_id = env.str("CANVAS_COURSE_ID")

    canvas = Canvas(env.str("CANVAS_URL"), env.str("CANVAS_TOKEN"))
    course = canvas.get_course(course_id)
    return base64.b64decode(course.uuid)


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """
    # Encode as bytes if provided string else just keep as byte string
    if isinstance(some_val, str):
        some_val = some_val.encode()
    else:
        some_val = some_val

    if isinstance(salt, str):
        salt = salt.encode()
    else:
        salt = salt

    return hashlib.sha256(salt + some_val).digest()


def get_user_id(username: str) -> str:
    salt = get_csci_salt() + get_csci_pepper()
    return hash_str(username.lower(), salt=salt).hex()[:8]
