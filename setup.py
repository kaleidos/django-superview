# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'django-superview',
    version = "0.4",
    description = "Generic View class with extra funionality for Django",
    long_description = "",
    keywords = 'django, view',
    author = 'Jesús Espino García & Andrei Antoukh',
    author_email = 'jespinog@gmail.com, niwi@niwi.be',
    url = 'https://github.com/kaleidos/django-superview',
    license = 'BSD',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'pytz',
    ],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
