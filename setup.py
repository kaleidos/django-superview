#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import superview

setup(
    name='superview',
    version=superview.get_version(),
    description="Generic View class with extra funionality for Django",
    long_description=open('README.rst', 'r').read(),
    keywords='django, view',
    author='Jesús Espino García & Sultan Imanhodjaev',
    author_email='jespinog@gmail.com, sultan.imanhodjaev@gmail.com',
    url='https://github.com/jespino/django-superview',
    license='LGPL',
    package_dir={'superview': 'superview'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
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
