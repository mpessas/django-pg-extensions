# -*- coding: utf-8 -*-

"""
Custom fields for postgresql.
"""

from django.db import models


class TsVectorField(models.Field):

    description = 'A tsvector field for full-text search.'

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['default'] = None
        kwargs['editable'] = False
        kwargs['serialize'] = False
        kwargs['db_index'] = True
        super(TsVectorField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'tsvector'


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['djangopg\.fields\.TsVectorField'])
except ImportError:
    pass
