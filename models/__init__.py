#!/usr/bin/python3
"""Initialize the storage module for the HBnB project."""
from models.engine.file_storage import FileStorage

unique_storage_instance = FileStorage()
unique_storage_instance.reload()
