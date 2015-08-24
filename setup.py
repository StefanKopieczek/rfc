from setuptools import setup

setup(name='rfc',
      version='0.1',
      description='View RFCs from the command line and store them offline.',
      url='http://github.com/stefankopieczek/rfc',
      author='Stefan Kopieczek',
      author_email='stefankopieczek+rfc@gmail.com',
      license='LGPL 2.0',
      packages=['rfc'],
      install_requires=['tabulate'],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'rfc = rfc.rfc:main'
          ]
      })
