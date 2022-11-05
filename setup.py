from setuptools import find_packages
from setuptools import setup

setup(name='movs-merger',
      version='0.0.0',
      url='https://github.com/ZeeD/movs-merger',
      author='Vito De Tullio',
      author_email='vito.detullio@gmail.com',
      py_modules=find_packages(),
      install_requires=[
          'movs'
      ],
      package_data={
          'movsmerger': ['py.typed'],
      },
      entry_points={
          'console_scripts': [
              'movs-merger = movsmerger:main'
          ]
      })
