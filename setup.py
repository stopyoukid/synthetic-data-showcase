#!/usr/bin/env python

from distutils.core import setup

setup(name='synthetic_data_showcase',
      version='0.1',
      description='Generates synthetic data and user interfaces for privacy-preserving data sharing and analysis.',
      author='Darren Edge',
      author_email='darren.edge@microsoft.com',
      license='MIT',
      url='https://github.com/microsoft/synthetic-data-showcase',
      packages=['sythetic_data'],
      install_requires=[
          'pandas==1.2.*',
          'matplotlib==3.2.*',
          'seaborn==0.10.*',
          'psutil==5.7.*',
          'joblib==0.14.*'
      ],
)
