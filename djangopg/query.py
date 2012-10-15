# -*- coding: utf-8 -*-

import types
from django.db.models import Q
from django.db.models.sql.constants import LOOKUP_SEP
from django.core.exceptions import FieldError
from django.db.models.sql.where import AND
from djangopg.where import RelabeledWhereNode


class SearchQ(Q):
    """
    A Q object for full-text search.

    Usage:
        SearchQ(field__fts='string of terms')
    """

    lookup_types = ['fts', ]

    def __init__(self, *args, **kwargs):
        self.config=kwargs.pop('config', 'pg_catalog.simple')
        self.include_order = kwargs.pop('include_order', False)
        super(SearchQ, self).__init__(*args, **kwargs)

    def add_to_query(self, query, used_aliases):
        arg, value = self.children[0]
        if not isinstance(value, types.StringTypes):
            raise ValueError('The value needs to be of type string')
        parts = arg.split(LOOKUP_SEP)
        if not parts:
            raise FieldError("Cannot parse keyword query %r" % arg)
        lookup_type = parts.pop()
        if not parts:
            raise FieldError("No suffix used in field")

        opts = query.get_meta()
        alias = query.get_initial_alias()
        field, target, opts, join_list, last, extra_filters = query.setup_joins(
            parts, opts, alias, True, True
        )

        # Mimick connection.ops.quote_name
        column_name = '"%%s"."%s_fts"' % target.column
        table_name = join_list[-1]
        raw_sql = "%s @@ plainto_tsquery('%s', %%%%s)" % (column_name, self.config)
        query.where.add(
            RelabeledWhereNode(table_name, raw_sql, [value]), AND
        )

        if self.include_order:
            quoted_rank_col_name = '"%s"."%s_fts"' % (table_name, target.column)
            query_sql = "plainto_tsquery('%s', %%s)" % self.config
            select_clause = u'ts_rank(%s, %s)' %  (quoted_rank_col_name, query_sql)
            query.extra.update({'fts_rank': (select_clause % '%s', [value])})
