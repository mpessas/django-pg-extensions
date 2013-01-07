# -*- coding: utf-8 -*-

from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper


class DatabaseWrapper(DatabaseWrapper):
    """Custom database wrapper."""

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.operators.update(
            {
                'array_contains': '@> %s',
                'array_contained': '<@ %s',
                'array_overlaps': '&& %s',
            }
        )
