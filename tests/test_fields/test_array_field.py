# -*- coding: utf-8 -*-

import unittest
from djangopg.fields import ArrayField, CharArrayField, IntArrayField


class DbTypeTestCase(unittest.TestCase):
    """Tests for the db_type."""

    def test_type_is_always_array(self):
        f = ArrayField()
        setattr(f, '_type', 'int')
        self.assertIn('[]', f.db_type(None))

    def test_respects_type_of_class(self):
        custom_type = 'int'
        f = ArrayField()
        setattr(f, '_type', custom_type)
        self.assertIn(custom_type, f.db_type(None))


class OperatorsTestCase(unittest.TestCase):
    """Tests for the allowed operators."""

    def test_invalid_operator_raises_type_error(self):
        f = ArrayField()
        self.assertRaises(TypeError, f.get_prep_lookup, 'contains', 'str')

    def test_valid_operators_return_value(self):
        value = [1, 2, 3, ]
        f = ArrayField()
        for op in ArrayField._allowed_operators:
            self.assertEqual(value, f.get_prep_lookup(op, value))


class PythonValueTestCase(unittest.TestCase):
    """Tests for converting the database value to Python type."""

    def setUp(self):
        self.f = ArrayField()

    def test_none_returns_none(self):
        self.assertIsNone(self.f.to_python(None))

    def test_empty_list_returns_empty_list(self):
        self.assertEqual(self.f.to_python([]), [])

    def test_list_returns_list(self):
        self.assertEqual(self.f.to_python([1, 2]), [1, 2])


class ConversionToPythonTestCase(unittest.TestCase):
    """Test specific conversion to django types."""

    def test_populated_array_of_varchar_returns_list_of_unicode(self):
        f = CharArrayField()
        res = f.to_python(['a', 'b'])
        self.assertIsInstance(res, list)
        for element in res:
            self.assertIsInstance(element, unicode)

    def test_populated_array_of_int_returns_list_of_int(self):
        f = IntArrayField()
        res = f.to_python([1, 2])
        self.assertIsInstance(res, list)
        for element in res:
            self.assertIsInstance(element, int)


class DbValueTestCase(unittest.TestCase):
    """Tests for converting the Python value to database type."""

    def setUp(self):
        self.f = ArrayField()

    def test_none_returns_none(self):
        # psycopg2 will convert None to NULL
        self.assertIsNone(self.f.get_prep_value(None))

    def test_empty_list_returns_empty_list(self):
        # psycopg2 will convert [] to {}
        self.assertEqual(self.f.get_prep_value([]), [])

    def test_list_returns_list(self):
        value = [1, 2, 3, ]
        self.assertEqual(self.f.get_prep_value(value), value)
