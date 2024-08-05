#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=False)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=False)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_valid_class_and_id_string(self):
        """Test get method with valid class and id, where class is a string"""
        # Create an object
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Get the object using get method
        retrieved_obj = models.storage.get("State", obj.id)

        # Assert that the retrieved object is not None and matches the original object
        self.assertIsNotNone(retrieved_obj)
        self.assertEqual(retrieved_obj.id, obj.id)
        self.assertEqual(retrieved_obj.name, obj.name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_invalid_class_and_valid_id(self):
        """Test get method with invalid class and valid id"""
        # Create an object
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Try to get the object using an invalid class name
        retrieved_obj = models.storage.get("InvalidClass", obj.id)

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_valid_class_and_invalid_id(self):
        """Test get method with valid class and invalid id"""
        # Create an object
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Try to get the object using a valid class name but an invalid id
        retrieved_obj = models.storage.get("State", "invalid_id")

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_none_class_and_invalid_id(self):
        """Test get method with class as None and invalid id"""
        # Create an object
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Try to get the object using None as the class name and an invalid id
        retrieved_obj = models.storage.get(None, "invalid_id")

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_valid_class_and_id_but_no_object_exists(self):
        """
        Test get method with valid class and id,
        but object does not exist in database
        """
        # Create an object with a known id
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Try to get the object using the same id but a different object type
        retrieved_obj = models.storage.get("City", obj.id)

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_nonexistent_class_as_string(self):
        """
        Test get method with class as a string,
        but class does not exist in classes dictionary
        """
        db_storage = DBStorage()
        db_storage.reload()

        # Try to get an object using a nonexistent class name as a string
        retrieved_obj = db_storage.get("NonexistentClass", "any_id")

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

        db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_nonexistent_class_as_object(self):
        """
        Test get method with class as a class object,
        but class does not exist in database
        """
        db_storage = DBStorage()
        db_storage.reload()

        # Define a nonexistent class for testing
        class NonexistentClass:
            pass

        # Try to get an object using a nonexistent class as a class object
        retrieved_obj = db_storage.get(NonexistentClass, "any_id")

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

        db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_none_class_and_valid_id(self):
        """Test get method with class as None and valid id"""
        # Create an object
        obj = State(name="Test State")
        models.storage.new(obj)
        models.storage.save()

        # Try to get the object using None as the class name
        retrieved_obj = models.storage.get(None, obj.id)

        # Assert that the retrieved object is None
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_nonexistent_class(self):
        """Test count method with a non-existent class"""
        db_storage = DBStorage()
        db_storage.reload()

        # Define a nonexistent class for testing
        class NonexistentClass:
            pass

        # Try to count objects using a nonexistent class as a class object
        count = db_storage.count(NonexistentClass)

        # Assert that the count is 0
        self.assertEqual(count, 0)

        db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_class_with_no_objects(self):
        """
        Test count method with a class that
        has no objects in the database
        """
        db_storage = DBStorage()
        db_storage.reload()

        # Create a class with no objects in the database
        class NoObjectsClass:
            pass

        # Try to count objects using the class with no objects
        count = db_storage.count(NoObjectsClass)

        # Assert that the count is 0
        self.assertEqual(count, 0)

        db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_valid_class_and_nonexistent_id(self):
        """Test count method with a valid class and a non-existent ID"""
        db_storage = DBStorage()
        db_storage.reload()

        # Create an object with a known id
        obj = State(name="Test State")
        db_storage.new(obj)
        db_storage.save()

        # Try to count objects using a valid class name but a non-existent id
        count = db_storage.count(State)

        # Assert that the count is1(since only the object with known id exists)
        self.assertEqual(count, 1)

        db_storage.close()
