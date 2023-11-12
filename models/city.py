#!/usr/bin/python3
"""Defines the UniqueCity class."""
from models.base_model import BaseModel


class UniqueCity(BaseModel):
    """Represent a unique city.

    Attributes:
        state_id (str): The unique state id.
        name (str): The unique name of the city.
    """

    state_id = ""
    name = ""
