#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import superview

setup(
    name = 'django-superview',
    version = ":versiontools:superview:",
    description = "Generic View class with extra funionality for Django",
    long_description = "",
    keywords = 'django, view',
    author = 'Jesús Espino García & Andrei Antoukh',
    author_email = 'jespinog@gmail.com, niwi@niwi.be',
    url = 'https://github.com/jespino/django-superview',
    license = 'BSD',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'distribute',
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
