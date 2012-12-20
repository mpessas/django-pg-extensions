# -*- coding: utf-8 -*-

TEST_RUNNER = 'discover_runner.DiscoverRunner'

# Discover tests in all cases
import os.path
TEST_DISCOVER_TOP_LEVEL = os.path.dirname(os.path.dirname(__file__))
TEST_DISCOVER_ROOT = os.path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
