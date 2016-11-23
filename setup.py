#!/usr/bin/env python
from setuptools import setup


setup(
    name='openrazer',
    version='0.0.1',
    description='A simple interface for openrazer keyboards',
    author='Danny Lawrence',
    author_email='dannyla@linux.com',
    url='https://github.com/daniellawrence/openrazer-python',
    packages=['openrazer'],
    long_description="https://github.com/daniellawrence/openrazer-python",
    entry_points={
        'console_scripts': [
            'razercli = openrazer.cli:razer_cli',
        ],
    },
)
