#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='logparser',
    version='0.1.0',
    author='Josh Reichardt',
    description='A command line tool for processing S3 ALB logs',
    long_description=open('README.md').read(),
    url='https://github.com/jmreicha/s3-alb-logparser',
    install_requires=['click', 'boto3', 'smart_open'],
    entry_points={
        'console_scripts':[
            'logparser = logparser.cli:logparser',
            ],
        },
    )
