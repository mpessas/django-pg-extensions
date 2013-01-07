# -*- coding: utf-8 -*-

from django.db.models.sql import Query

Query.query_terms.update(
    {
        'array_contains': None, 'array_contained': None, 'array_overlaps': None
    }
)
