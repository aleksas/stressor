#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from os import path
    from setuptools import setup, find_packages
    from setuptools.dist import Distribution
except ImportError:
    from distutils.core import setup

from phonology_engine.version import VERSION
__version__ = VERSION

try:
    if sys.version_info[:2] <= (2, 7):
        readme = open("README.md")
    else:
        readme = open("README.md", encoding="utf8")
    long_description = str(readme.read())
finally:
    readme.close()

setup(
    name='phonology_engine',
    author='Aleksas Pielikis',
    version=VERSION,
    author_email='ant.kampo@gmail.com',
    description="Module to get stress and syllables for words in a given sentence in Lithuanian language.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aleksas/phonology_engine',
    license='BSD',
    packages=['phonology_engine', 'phonology_engine.tests'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['phonology_engine', 'phonology', 'pronunciation', 'stress', 'syllable', 'accent', 'hyphenation'],
    package_data={
        'phonology_engine': [
            'Linux_x86_64/libPhonologyEngine.so',
            'Linux_x86/libPhonologyEngine.so',
            'Win32_x86/PhonologyEngine.dll',
            'Win64_x64/PhonologyEngine.dll'],
    }
)
