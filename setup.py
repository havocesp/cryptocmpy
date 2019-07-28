# -*- coding:utf-8 -*-
""" Setup file."""

import os

import setuptools

exclude = ['.mypy*', '.idea*', 'build*', '{}.egg-info*'.format(__package__), 'dist*', 'venv*', 'docs*', 'lab*']

keywords = ['altcoins', 'altcoin', 'exchange', 'mining', 'cryptocompare', 'crypto', 'compare', 'api', 'wrapper']

root_dir = os.path.dirname(__file__)
readme_file = os.path.join(root_dir, 'README.md')
long_description = str()
if os.path.isfile(readme_file):
    with open(readme_file) as fp:
        long_description = fp.read()

setuptools.setup(
    name='cryptocmpy',
    version='0.1.2',
    packages=setuptools.find_packages(exclude=exclude),
    url='github.com/havocesp/cryptocmpy',
    license='UNLICENSE',
    keywords=keywords,
    author='Daniel J. Umpierrez',
    author_email='umpierrez@pm.me',
    long_description=long_description,
    description='Python 3 "CryptoCompare" site API wrapper.',
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
