#!/usr/bin/env python

from setuptools import setup

setup(
    name='toolbot',
    version='1.0',
    description="",
    author="Thom Gerdes",
    author_email="tgerdes@gmail.com",
    packages=['toolbot'],
    install_requires=["aiohttp", "flask", "irc3"],
    license="MIT",
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Framework :: Flask',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
        'Topic :: Communications :: Chat',
    ),
)
