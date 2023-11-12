#!/usr/bin/python3
"""Defines the Accommodation class."""
from models.base_model import BaseModel


class Accommodation(BaseModel):
    """Represent an accommodation.

    Attributes:
        city_identity (str): The City identity.
        host_identity (str): The Host identity.
        title (str): The title of the accommodation.
        description (str): The description of the accommodation.
        room_count (int): The number of rooms in the accommodation.
        bathroom_count (int): The number of bathrooms in the accommodation.
        guest_capacity (int): The maximum guest capacity of the accommodation.
        nightly_price (int): The price per night for the accommodation.
        latitude (float): The latitude of the accommodation.
        longitude (float): The longitude of the accommodation.
        amenity_identity_list (list): A list of Amenity identities.
    """

    city_identity = ""
    host_identity = ""
    title = ""
    description = ""
    room_count = 0
    bathroom_count = 0
    guest_capacity = 0
    nightly_price = 0
    latitude = 0.0
    longitude = 0.0
    amenity_identity_list = []
