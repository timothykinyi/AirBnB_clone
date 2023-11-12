#!/usr/bin/python3
"""Defines the UniqueUser class."""
from models.base_model import BaseModel


class UniqueUser(BaseModel):
    """Represent a unique user.

    Attributes:
        user_email (str): The email of the user.
        user_password (str): The password of the user.
        user_first_name (str): The first name of the user.
        user_last_name (str): The last name of the user.
    """

    user_email = ""
    user_password = ""
    user_first_name = ""
    user_last_name = ""
