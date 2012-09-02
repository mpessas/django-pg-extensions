# -*- coding: utf-8 -*-

from django.db import models, connections
from django.utils.encoding import force_unicode


class FtsQuerySet(models.query.QuerySet):

    def search(self, **kwargs):
        """Do a full-text search."""
        where = []
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

            func_name = 'plainto_tsquery'
            ts_query = "%s('%s', '%s')" % (
                func_name, config, force_unicode(query).replace("'","''")
            )
            qn = connections[self.db].ops.quote_name
            field = '{table}.{column}'.format(
                table=qn(db_table), column=qn(search_field))
            where.append(unicode(" ({0}) @@ ({1})".format(field, ts_query)))

        return self.extra(where=where)
