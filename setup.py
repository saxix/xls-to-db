#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import find_packages, setup
rel = lambda fname: os.path.join(os.path.dirname(__file__),
                                 'src',
                                 'requirements', fname)


def fread(fname):
    return open(rel(fname)).read()

install_requires = fread('install.pip')
test_requires = fread('testing.pip')
dev_requires = fread('develop.pip')


readme = codecs.open('README.rst').read()
history = codecs.open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(name='xls-to-db',
      version="0.1",
      description="""XLS to DB. Load xls into your favorite database""",
      long_description=readme + '\n\n' + history,
      author='Stefano Apostolico',
      author_email='s.apostolico@gmail.com',
      url='https://github.com/saxix/',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      install_requires=install_requires,
      tests_require=dev_requires,
      extras_require={
          'dev': dev_requires,
          'tests': test_requires,
          'cli': ['click==6.7',],
      },
      entry_points={
          'console_scripts': [
              'xls-to-db = xls_to_db.cli:cli',
          ],
      },
      license="BSD",
      zip_safe=False,
      keywords='mercury',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.6',
      ])
