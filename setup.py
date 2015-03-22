# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup

VERSION = '0.1'


def get_long_description():
    desc = ''
    with open('README.rst') as f:
        desc = f.read()
    return desc


setup(
    name='transmissiontransfer',
    version=VERSION,
    description='Moves torrents from one transmission instance to another',
    long_description=get_long_description(),
    keywords='torrent transmission',
    author='Matthew Wilkes',
    author_email='matt@matthewwilkes.name',
    url='https://github.com/matthewwilkes/transmissiontransfer',
    license='GPL',
    install_requires=[
        'transmissionrpc',
    ],
    entry_points={
        'console_scripts': [
            'transmissiontransfer = transmissiontransfer:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
)