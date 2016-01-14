# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="django-pg-extensions",
    version="0.1.7",
    description="Extensions for Django to fully utilize PostgreSQL.",
    author="Apostolos Bessas",
    author_email="mpessas@gmail.com",
    packages=["djangopg", "djangopg.postgresql_psycopg2", ],
    install_requires=["Django", ],
    tests_require=["django-discover-runner", "mock", ]
)
