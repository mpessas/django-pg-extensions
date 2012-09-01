# -*- coding: utf-8 -*-

from django.db import models, connections
from django.utils.encoding import force_unicode


class FtsQuerySet(models.query.QuerySet):

    def search(self, **kwargs):
        search_field, query = kwargs.items()[0]
        config_var = search_field + '_config'
        config = getattr(self.model._meta, config_var, 'pg_catalog.simple')
        qn = connections[self.db].ops.quote_name

        func_name = 'plainto_tsquery'
        ts_query = "%s('%s', '%s')" % (
            func_name, config, force_unicode(query).replace("'","''")
        )
        field = '{table}.{column}'.format(
            table=qn(self.model._meta.db_table), column=qn(search_field))
        where = unicode(" ({0}) @@ ({1})".format(field, ts_query))

        return self.extra(where=[where])
