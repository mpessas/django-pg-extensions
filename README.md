# Django PostgreSQL Extensions

This package tries to expose functionality from PostgreSQL to django
applications.


Python 2.6 or greater is required.


## Features

- Support for the full text search engine of PostgreSQL.
- Support for the COPY command.
- Support for ARRAYs. Out of the box support for INT and TEXT arrays. The
  operators @> (contains), <@ (is contained by) and && (overlaps with) are
  supported.
- Case-insensitive variants of `CharField` and `SlugField`.


## Running the tests

Just run

    django-admin.py test --settings=djangopg.test_settings

from the root directory.
