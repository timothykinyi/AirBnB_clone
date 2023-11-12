#!/usr/bin/python3
"""Defines the GeographicRegion class."""
from models.base_model import BaseModel


class GeographicRegion(BaseModel):
    """Represent a geographic region.

    Attributes:
        region_name (str): The name of the geographic region.
    """

    region_name = ""
