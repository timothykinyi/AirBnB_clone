#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorageInstantiation
    TestFileStorageMethods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_instantiation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initialized(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)

        for instance in instances:
            key = "{}.{}".format(instance.__class__.__name__, instance.id)
            self.assertIn(key, models.storage.all())
            self.assertEqual(models.storage.all()[key], instance)

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)

        models.storage.save()

        with open("file.json", "r") as f:
            save_data = json.load(f)

        for instance in instances:
            key = "{}.{}".format(instance.__class__.__name__, instance.id)
            self.assertIn(key, save_data)
            self.assertEqual(save_data[key], instance.to_dict())

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)

        models.storage.save()
        models.storage.reload()

        for instance in instances:
            key = "{}.{}".format(instance.__class__.__name__, instance.id)
            self.assertIn(key, models.storage.all())
            self.assertEqual(models.storage.all()[key].to_dict(), instance.to_dict())

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
