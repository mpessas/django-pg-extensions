# -*- coding: utf-8 -*-

from django.db import models
from djangopg.querysets import FtsQuerySet


class FtsManagerMixin(object):

    def __init__(self, search_field):
        self._search_field = search_field
        super(FtsManagerMixin, self).__init__()

    def get_query_set(self):
        return FtsQuerySet(self.model, using=self._db).defer(self._search_field)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), name)
