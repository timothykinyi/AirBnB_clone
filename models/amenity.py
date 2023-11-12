#!/usr/bin/python3
"""Defines the UniqueAmenity class."""
from models.base_model import BaseModel


class UniqueAmenity(BaseModel):
    """Represent a uniquely defined amenity.

    Attributes:
        feature (str): The unique feature of the amenity.
    """

    feature = ""
