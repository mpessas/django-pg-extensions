# -*- coding: utf-8 -*-

from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper
from django.db.backends.postgresql_psycopg2.operations import (
    DatabaseOperations as BaseOperations
)


class DatabaseOperations(BaseOperations):

    def lookup_cast(self, lookup_type):
        lookup = '%s'
        # Use UPPER(x) for case-insensitive lookups; it's faster.
        if lookup_type in ('iexact', 'icontains', 'istartswith', 'iendswith'):
            lookup = 'UPPER(%s)' % lookup
        return lookup


class DatabaseWrapper(DatabaseWrapper):
    """Custom database wrapper."""

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.ops = DatabaseOperations(self)
        self.operators.update(
            {
                'array_contains': '@> %s',
                'array_contained': '<@ %s',
                'array_overlaps': '&& %s',
            }
        )
