# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode


class ArrayField(models.Field):
    """Base class for fields of type array."""

    __metaclass__ = models.SubfieldBase

    _allowed_operators = ['exact', 'isnull', ]

    def db_type(self, connection):
        return '%s[]' % self._type

    def to_python(self, value):
        # Psycopg2 uses lists for arrays
        if value is None or value == '':
            # The check for empty strings is needed, because to_python
            # is called on empty constructors.
            return None
        if not isinstance(value, list):
            raise TypeError("Expected list, got %s" % type(value))
        return value

    def get_prep_value(self, value):
        return value

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type not in self._allowed_operators:
            raise TypeError('Invalid operator %s' % lookup_type)
        return super(ArrayField, self).get_prep_lookup(lookup_type, value)


class CharArrayField(ArrayField):
    """Field for arrays of VARCHAR."""

    description = 'VARCHAR array'
    _type = 'varchar'

    def to_python(self, value):
        value = super(CharArrayField, self).to_python(value)
        if value is None:
            return None
        return map(smart_unicode, value)


class IntArrayField(ArrayField):
    """Field for arrays of INT."""

    description = 'INT array'
    _type = 'int'
