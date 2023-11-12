#!/usr/bin/python3
"""Defines the GuestReview class."""
from models.base_model import BaseModel


class GuestReview(BaseModel):
    """Represent a guest review.

    Attributes:
        accommodation_id (str): The Accommodation id.
        reviewer_id (str): The Reviewer id.
        feedback_text (str): The text of the guest review.
    """

    accommodation_id = ""
    reviewer_id = ""
    feedback_text = ""
