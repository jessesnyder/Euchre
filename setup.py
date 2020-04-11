"""Minimal setup file"""

from setuptools import setup, find_packages

setup(
    name='euchre',
    version='0.1.0',
    description='A Euchre game',

    author='Colin Ong-Dean',
    author_email='',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[],
    extras_require={},

    # entry_points={
    #     'console_scripts': [
    #         'tasks = tasks.cli:tasks_cli',
    #     ]
    # },
)
