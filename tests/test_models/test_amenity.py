#!/usr/bin/python3
"""Unit tests for the Amenity class in the models module.

Test classes:
    TestAmenityInstantiation
    TestAmenitySave
    TestAmenityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity as AmenityModel


class TestAmenityInstantiation(unittest.TestCase):
    """Unit tests for the instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(AmenityModel, type(AmenityModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(AmenityModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(AmenityModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(AmenityModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(AmenityModel().updated_at))

    def test_name_is_public_class_attribute(self):
        amenity_instance = AmenityModel()
        self.assertEqual(str, type(AmenityModel.name))
        self.assertIn("name", dir(AmenityModel()))
        self.assertNotIn("name", amenity_instance.__dict__)

    def test_two_amenities_unique_ids(self):
        amenity1 = AmenityModel()
        amenity2 = AmenityModel()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_two_amenities_different_created_at(self):
        amenity1 = AmenityModel()
        sleep(0.05)
        amenity2 = AmenityModel()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_two_amenities_different_updated_at(self):
        amenity1 = AmenityModel()
        sleep(0.05)
        amenity2 = AmenityModel()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        current_datetime = datetime.today()
        datetime_repr = repr(current_datetime)
        amenity_instance = AmenityModel()
        amenity_instance.id = "123456"
        amenity_instance.created_at = amenity_instance.updated_at = current_datetime
        amenity_str = amenity_instance.__str__()
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + datetime_repr, amenity_str)
        self.assertIn("'updated_at': " + datetime_repr, amenity_str)

    def test_args_unused(self):
        amenity_instance = AmenityModel(None)
        self.assertNotIn(None, amenity_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Instantiation with kwargs test method"""
        current_datetime = datetime.today()
        datetime_iso = current_datetime.isoformat()
        amenity_instance = AmenityModel(id="345", created_at=datetime_iso, updated_at=datetime_iso)
        self.assertEqual(amenity_instance.id, "345")
        self.assertEqual(amenity_instance.created_at, current_datetime)
        self.assertEqual(amenity_instance.updated_at, current_datetime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            AmenityModel(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """Unit tests for the save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        amenity_instance = AmenityModel()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        self.assertLess(first_updated_at, amenity_instance.updated_at)

    def test_two_saves(self):
        amenity_instance = AmenityModel()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        second_updated_at = amenity_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity_instance.save()
        self.assertLess(second_updated_at, amenity_instance.updated_at)

    def test_save_with_arg(self):
        amenity_instance = AmenityModel()
        with self.assertRaises(TypeError):
            amenity_instance.save(None)

    def test_save_updates_file(self):
        amenity_instance = AmenityModel()
        amenity_instance.save()
        amenity_id = "AmenityModel." + amenity_instance.id
        with open("file.json", "r") as file:
            self.assertIn(amenity_id, file.read())


class TestAmenityToDict(unittest.TestCase):
    """Unit tests for the to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(AmenityModel().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenity_instance = AmenityModel()
        self.assertIn("id", amenity_instance.to_dict())
        self.assertIn("created_at", amenity_instance.to_dict())
        self.assertIn("updated_at", amenity_instance.to_dict())
        self.assertIn("__class__", amenity_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenity_instance = AmenityModel()
        amenity_instance.middle_name = "Holberton"
        amenity_instance.my_number = 98
        self.assertEqual("Holberton", amenity_instance.middle_name)
        self.assertIn("my_number", amenity_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity_instance = AmenityModel()
        amenity_dict = amenity_instance.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        current_datetime = datetime.today()
        amenity_instance = AmenityModel()
        amenity_instance.id = "123456"
        amenity_instance.created_at = amenity_instance.updated_at = current_datetime
        expected_dict = {
            'id': '123456',
            '__class__': 'AmenityModel',
            'created_at': current_datetime.isoformat(),
            'updated_at': current_datetime.isoformat(),
        }
        self.assertDictEqual(amenity_instance.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        amenity_instance = AmenityModel()
        self.assertNotEqual(amenity_instance.to_dict(), amenity_instance.__dict__)

    def test_to_dict_with_arg(self):
        amenity_instance = AmenityModel()
        with self.assertRaises(TypeError):
            amenity_instance.to_dict(None)


if __name__ == "__main__":    unittest.main()
