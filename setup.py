#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from os import path
    from setuptools import setup, find_packages
    from setuptools.dist import Distribution
except ImportError:
    from distutils.core import setup

from sandara.version import VERSION
__version__ = VERSION


try:
    if sys.version_info[:2] <= (2, 7):
        readme = open("README.md")
    else:
        readme = open("README.md", encoding="utf8")
    long_description = str(readme.read())
finally:
    readme.close()

class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True

setup(
    name='sandara',
    author='Aleksas Pielikis',
    version=VERSION,
    author_email='ant.kampo@gmail.com',
    description="Module to get pronunciation and hyphenation for words in a given sentence in Lithuanian language",
    long_description=long_description,
    url='https://github.com/aleksas/sandara',
    license='BSD',
    packages=find_packages(exclude=['contrib', 'docs']),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['sandara', 'pronunciation', 'shyphenation'],
    package_data={
        'sandara': ['Linux_x86_64/libtranscrLUSS.so', 'Linux_x86_64/libTextNormalization.so'],
    },
    distclass=BinaryDistribution
)
