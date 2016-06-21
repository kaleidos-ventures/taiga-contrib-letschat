#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versiontools_support
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-letschat',
    version = ":versiontools:taiga_contrib_letschat:",
    description = "The Taiga plugin for LetsChat integration",
    long_description = "",
    keywords = 'taiga, letschat, integration',
    author = 'Andrea Stagi',
    author_email = 'stagi.andrea@gmail.com',
    url = 'https://github.com/taigaio/taiga-contrib-letschat',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[],
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
