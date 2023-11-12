#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestCustomModelInstantiation
    TestCustomModelSave
    TestCustomModelToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel as CustomModel


class TestCustomModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the CustomModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(CustomModel, type(CustomModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(CustomModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(CustomModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(CustomModel().updated_at))

    def test_two_models_unique_ids(self):
        cm1 = CustomModel()
        cm2 = CustomModel()
        self.assertNotEqual(cm1.id, cm2.id)

    def test_two_models_different_created_at(self):
        cm1 = CustomModel()
        sleep(0.05)
        cm2 = CustomModel()
        self.assertLess(cm1.created_at, cm2.created_at)

    def test_two_models_different_updated_at(self):
        cm1 = CustomModel()
        sleep(0.05)
        cm2 = CustomModel()
        self.assertLess(cm1.updated_at, cm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cm = CustomModel()
        cm.id = "123456"
        cm.created_at = cm.updated_at = dt
        cmstr = cm.__str__()
        self.assertIn("[CustomModel] (123456)", cmstr)
        self.assertIn("'id': '123456'", cmstr)
        self.assertIn("'created_at': " + dt_repr, cmstr)
        self.assertIn("'updated_at': " + dt_repr, cmstr)

    def test_args_unused(self):
        cm = CustomModel(None)
        self.assertNotIn(None, cm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cm = CustomModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cm.id, "345")
        self.assertEqual(cm.created_at, dt)
        self.assertEqual(cm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            CustomModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cm = CustomModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cm.id, "345")
        self.assertEqual(cm.created_at, dt)
        self.assertEqual(cm.updated_at, dt)


class TestCustomModelSave(unittest.TestCase):
    """Unittests for testing save method of the CustomModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        cm = CustomModel()
        sleep(0.05)
        first_updated_at = cm.updated_at
        cm.save()
        self.assertLess(first_updated_at, cm.updated_at)

    def test_two_saves(self):
        cm = CustomModel()
        sleep(0.05)
        first_updated_at = cm.updated_at
        cm.save()
        second_updated_at = cm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cm.save()
        self.assertLess(second_updated_at, cm.updated_at)

    def test_save_with_arg(self):
        cm = CustomModel()
        with self.assertRaises(TypeError):
            cm.save(None)

    def test_save_updates_file(self):
        cm = CustomModel()
        cm.save()
        cmid = "CustomModel." + cm.id
        with open("file.json", "r") as f:
            self.assertIn(cmid, f.read())


class TestCustomModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the CustomModel class."""

    def test_to_dict_type(self):
        cm = CustomModel()
        self.assertTrue(dict, type(cm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        cm = CustomModel()
        self.assertIn("id", cm.to_dict())
        self.assertIn("created_at", cm.to_dict())
        self.assertIn("updated_at", cm.to_dict())
        self.assertIn("__class__", cm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        cm = CustomModel()
        cm.name = "Holberton"
        cm.my_number = 98
        self.assertIn("name", cm.to_dict())
        self.assertIn("my_number", cm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        cm = CustomModel()
        cm_dict = cm.to_dict()
        self.assertEqual(str, type(cm_dict["created_at"]))
        self.assertEqual(str, type(cm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        cm = CustomModel()
        cm.id = "123456"
        cm.created_at = cm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'CustomModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(cm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        cm = CustomModel()
        self.assertNotEqual(cm.to_dict(), cm.__dict__)

    def test_to_dict_with_arg(self):
        cm = CustomModel()
        with self.assertRaises(TypeError):
            cm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
