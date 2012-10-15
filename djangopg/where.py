# -*- coding: utf-8 -*-


class RelabeledWhereNode(object):
    """
    WhereNode that supports both custom SQl and aliasing the table involved.
    """

    def __init__(self, table, sql, params):
        self.table = table
        self.sql = sql
        self.params = params

    def as_sql(self, qn=None, connection=None):
        return self.sql % self.table, self.params or ()

    def relabel_aliases(self, change_map, node=None):
        self.table = change_map.get(self.table, self.table)
