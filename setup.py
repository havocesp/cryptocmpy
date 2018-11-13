# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

import cryptocmpy as ccmp

exclude = ['.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'doc*', 'lab*']

setup(
    name=ccmp.__package__,
    version=ccmp.__version__,
    packages=find_packages(exclude=exclude),
    url=ccmp.__site__,
    license=ccmp.__license__,
    packages_dir={'': ccmp.__package__},
    keywords=ccmp.__keywords__,
    author=ccmp.__author__,
    author_email=ccmp.__email__,
    long_description=ccmp.__description__,
    description=ccmp.__description__,
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
