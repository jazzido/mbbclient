# encoding: utf-8
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='mbbclient',
      version=version,
      description="Cliente para los webservices publicados por la Municipalidad de Bahía Blanca",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
            'cmdln', 'lxml'
          ],
      entry_points={
          'console_scripts': [
              'mbbclient = mbbclient.mbb_client:main'
              ]
          },
      author='Manuel Aristarán',
      author_email='jazzido@jazzido.com',
      url='http://github.com/jazzido/mbbclient'
      )
