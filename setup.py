#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages
import os
import sys


# Get description from Readme file
readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme_file).read()

# Build a list with requirements of the app
REQUIRES = []
try:
    import django
except ImportError:
    # Because of the strange update behavior of "pip --upgrade package_name"
    # set requierment only if django not avallible.
    REQUIRES.append('django')

if sys.version_info < (3, 4):
   REQUIRES.append('python >= 3.4')


setup(name='django-onetimelink',
        version=0.2,
        description='A django one-time file streaming application',
        long_description=long_description,
        author='FENG Hao',
        author_email='hiroshifuu@outlook.com',
        url='https://github.com/HiroshiFuu/django-onetimelink',
        download_url='https://pypi.python.org/pypi/django-onetimelink',
        license='BSD',
        packages=find_packages(exclude=['example', ]),
        include_package_data=True,
        keywords="django one-time file link serve",
        classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Framework :: Django :: 2.0',
              'License :: OSI Approved :: BSD License',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 3 :: Only',
              'Environment :: Console',
              'Natural Language :: English',
              'Intended Audience :: Developers',
              'Topic :: Internet',
              ],
        install_requires=REQUIRES,
        zip_safe=False,
        )
