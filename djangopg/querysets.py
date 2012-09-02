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

    def _search(self, func_name, order_by_field=None, **kwargs):
        """Do a full-text search."""
        where = []
        select = {}
        order_by = []
        for search_field, query in kwargs.items():
            relation = None
            LOOKUP_SEP = models.sql.constants.LOOKUP_SEP
            if LOOKUP_SEP in search_field:
                # Assume one level for now
                relation, search_field = search_field.split(LOOKUP_SEP)

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

            ts_query = "%s('%s', '%s')" % (
                func_name, config, force_unicode(query).replace("'","''")
            )
            qn = connections[self.db].ops.quote_name
            field = '{table}.{column}'.format(
                table=qn(db_table), column=qn(search_field))
            where.append(u" ({0}) @@ ({1})".format(field, ts_query))

            if order_by_field is not None:
                if relation is None:
                    order_key = search_field
                else:
                    order_key = relation + LOOKUP_SEP + search_field
                order = order_by_field.get(order_key)
                if order is None:
                    continue
                if order.startswith('-'):
                    order = order[1:]
                    sign = '-'
                else:
                    sign = ''
                select[order] = u'ts_rank({0}, {1})'.format(field, ts_query)
                order_by.append(
                    '{sign}{field}'.format(sign=sign, field=order)
                )
        return self.extra(select=select, where=where, order_by=order_by)
