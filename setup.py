#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


def get_version(file_rel_path):
    base_dir = os.path.dirname(__file__)
    file_abs_path = os.path.join(base_dir, file_rel_path)
    with open(file_abs_path) as file:
        file_content = file.read()
        version = re.findall(r"^__version__ = '(.+)'$", file_content, re.MULTILINE)[0]
        return version


setup(
    name='vkstreaming',
    version=get_version('vkstreaming/__init__.py'),
    author='Daniil Suvorov',
    author_email='severecloud@gmail.com',

    url='https://github.com/SevereCloud/vk-streaming',
    download_url='https://github.com/SevereCloud/vk-streaming/archive/master.zip',
    description='vk streaming API Python',

    packages=find_packages(),
    install_requires=[
        'requests',
        'websocket-client'
    ],

    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='vk.com vk streaming api',
)
