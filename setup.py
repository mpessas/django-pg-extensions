# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = "django-pg-extensions",
    version = "0.1devel",
    description = "Extensions for Django to fully utilize PostgreSQL.",
    author = "Apostolos Bessas",
    author_email = "mpessas@gmail.com",
    packages=["djangopg"],
    install_requires=["Django", ],
    tests_require=["django-discover-runner", "mock", ]
)
