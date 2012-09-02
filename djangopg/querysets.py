# -*- coding: utf-8 -*-

from django.db import models, connections
from django.utils.encoding import force_unicode


class FtsQuerySet(models.query.QuerySet):

    def search_raw(self, **kwargs):
        """
        Do a raw full-text search.

        The user may also specify to order the results on how relevant they
        are. For this, he has to specify a keyword argument,
        ``order_by_field``. Using a minus in the field to control the
        ordering also works.
        """
        return self._search("to_tsquery", **kwargs)

    def search(self, **kwargs):
        """
        Do a full-text search.

        The user may also specify to order the results on how relevant they
        are. For this, he has to specify a keyword argument,
        ``order_by_field``. Using a minus in the field to control the
        ordering also works.
        """
        return self._search("plainto_tsquery", **kwargs)

    def _search(self, func_name, include_rank=False, **kwargs):
        """Do a full-text search."""
        where = []
        select = {}
        params = []
        for full_search_field, query in kwargs.items():
            LOOKUP_SEP = models.sql.constants.LOOKUP_SEP
            if LOOKUP_SEP in full_search_field:
                # Assume one level for now
                relation, search_field = full_search_field.split(LOOKUP_SEP)
            else:
                relation = None
                search_field = full_search_field

            config_var = search_field + '_config'
            default_config = 'pg_catalog.simple'
            if relation is None:
                db_table = self.model._meta.db_table
                config = getattr(self.model, config_var, default_config)
                self.query.join((None, db_table, None, None))
            else:
                related_model = getattr(self.model, relation).field.rel.to
                db_table = related_model._meta.db_table
                config = getattr(related_model, config_var, default_config)
                connection = (
                    self.model._meta.db_table, db_table,
                    getattr(self.model, relation).field.attname,
                    getattr(self.model, relation).field.rel.field_name
                )
                self.query.join(connection)

            ts_query = "{0}('{1}', %s)".format(func_name, config)
            params.append(query)
            qn = connections[self.db].ops.quote_name
            field = '{table}.{column}'.format(
                table=qn(db_table), column=qn(search_field))
            where.append(u" ({0}) @@ ({1})".format(field, ts_query))

            if include_rank:
                select_clause = u'ts_rank({0}, {1})'.format(field, ts_query)
                select[full_search_field + '_fts_rank'] = select_clause

        return self.extra(
            select=select, where=where, select_params=params, params=params
        )
