# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

import cryptocmpy as ccmpy

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']

setup(
    name=ccmpy.__package__,
    version=ccmpy.__version__,
    packages=find_packages(exclude=exclude),
    url=ccmpy.__site__,
    license=ccmpy.__license__,
    packages_dir={'': ccmpy.__package__},
    keywords=ccmpy.__keywords__,
    author=ccmpy.__author__,
    author_email=ccmpy.__email__,
    long_description=ccmpy.__description__,
    description=ccmpy.__description__,
    classifiers=[
        'Development Status :: 5 - Production',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests'
    ]
)
