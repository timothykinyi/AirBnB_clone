#!/usr/bin/python3
"""Defines the UniqueBaseModel class."""
import json
from uuid import uuid4
from datetime import datetime
import models


class UniqueBaseModel:
    """Represents a uniquely defined BaseModel for a custom project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new UniqueBaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.unique_id = str(uuid4())
        self.creation_date = datetime.today()
        self.last_update = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "creation_date" or k == "last_update":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def update(self):
        """Update last_update with the current datetime."""
        self.last_update = datetime.today()
        models.storage.save()

    def to_custom_dict(self):
        """Return a custom dictionary representation of the UniqueBaseModel instance.

        Includes the key/value pair __custom_class__ representing
        the custom class name of the object.
        """
        rdict = self.__dict__.copy()
        rdict["creation_date"] = self.creation_date.isoformat()
        rdict["last_update"] = self.last_update.isoformat()
        rdict["__custom_class__"] = self.__class__.__name__
        return rdict

    def __custom_str__(self):
        """Return the custom print/str representation of the UniqueBaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.unique_id, self.__dict__)


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_custom_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__custom_class__"]
                    del o["__custom_class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
