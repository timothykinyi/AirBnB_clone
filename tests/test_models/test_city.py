#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestUniqueCityInstantiation
    TestUniqueCitySave
    TestUniqueCityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestUniqueCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city_instance))
        self.assertNotIn("state_id", city_instance.__dict__)

    def test_name_is_public_class_attribute(self):
        city_instance = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city_instance))
        self.assertNotIn("name", city_instance.__dict__)

    def test_two_cities_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_two_cities_different_created_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_two_cities_different_updated_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city_instance = City()
        city_instance.id = "654321"
        city_instance.created_at = city_instance.updated_at = dt
        city_str = city_instance.__str__()
        self.assertIn("[City] (654321)", city_str)
        self.assertIn("'id': '654321'", city_str)
        self.assertIn("'created_at': " + dt_repr, city_str)
        self.assertIn("'updated_at': " + dt_repr, city_str)

    def test_args_unused(self):
        city_instance = City(None)
        self.assertNotIn(None, city_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city_instance = City(id="987", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city_instance.id, "987")
        self.assertEqual(city_instance.created_at, dt)
        self.assertEqual(city_instance.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city_instance = City("789", id="987", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city_instance.id, "987")
        self.assertEqual(city_instance.created_at, dt)
        self.assertEqual(city_instance.updated_at, dt)


class TestUniqueCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("unique_file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("unique_file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "unique_file.json")
        except IOError:
            pass

    def test_one_save(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        self.assertLess(first_updated_at, city_instance.updated_at)

    def test_two_saves(self):
        city_instance = City()
        sleep(0.05)
        first_updated_at = city_instance.updated_at
        city_instance.save()
        second_updated_at = city_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city_instance.save()
        self.assertLess(second_updated_at, city_instance.updated_at)

    def test_save_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.save(None)

    def test_save_updates_file(self):
        city_instance = City()
        city_instance.save()
        city_id = "City." + city_instance.id
        with open("unique_file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestUniqueCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        city_instance = City()
        self.assertTrue(dict, type(city_instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        city_instance = City()
        self.assertIn("id", city_instance.to_dict())
        self.assertIn("created_at", city_instance.to_dict())
        self.assertIn("updated_at", city_instance.to_dict())
        self.assertIn("__class__", city_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city_instance = City()
        city_instance.middle_name = "UniqueCity"
        city_instance.my_number = 123
        self.assertEqual("UniqueCity", city_instance.middle_name)
        self.assertIn("my_number", city_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city_instance = City()
        city_dict = city_instance.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        city_instance = City()
        city_instance.id = "456789"
        city_instance.created_at = city_instance.updated_at = dt
        t_dict = {
            'id': '456789',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city_instance.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        city_instance = City()
        self.assertNotEqual(city_instance.to_dict(), city_instance.__dict__)

    def test_to_dict_with_arg(self):
        city_instance = City()
        with self.assertRaises(TypeError):
            city_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
