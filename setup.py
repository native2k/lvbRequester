#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
# history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='lvbRequester',
    version='0.1.1',
    description='small library to request information from LVB (l.de) website',
    long_description=readme,
    author='Sven Richter',
    author_email='native2k@gmail.com',
    url='https://github.com/native2k/lvbRequester',
    packages=[
        'lvbRequester',
    ],
    package_dir={'lvbRequester': 'lvbRequester'},
    include_package_data=True,
    install_requires=[
        'requests',
        'egenix-mx-base',
        'urllib',
        'future',
    ],
    license="BSD",
    zip_safe=False,
    keywords='lvbRequester',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
