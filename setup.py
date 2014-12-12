#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="combo_runner",
    version=version,
    packages=find_packages(),
    description="combo runner for test automation",
    author="Mozilla Taiwan",
    author_email="tw-qa@mozilla.com",
    license="MPL",
    package_data={'': ['common/*'] },
    include_package_data=True,
    zip_safe=False,
)
