from setuptools import setup
import os

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = ''

setup(name='browserid',
      version='1.1',
      description="Mozilla BrowserID (Persona) Page Object Model",
      long_description=description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Mozilla Web QA',
      author_email='mozwebqa@mozilla.org',
      url='https://github.com/mozilla/bidpom',
      license='MPL 2.0',
      packages=['browserid', 'browserid.pages'],
      include_package_data=True)
