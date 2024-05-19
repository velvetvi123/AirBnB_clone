#!/usr/bin/python3
"""Defines state class"""
from models.base_model import BaseModel


class State(BaseModel):
    """Represent a state

    Attributes:
        name (str): the name of the state
    """

    name = ""
