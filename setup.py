from setuptools import setup

setup(name='bidpom',
      version='2.0.1',
      description='Mozilla BrowserID (Persona) Page Object Model',
      long_description=open('README.rst').read(),
      author='Mozilla Web QA',
      author_email='mozwebqa@mozilla.org',
      url='https://github.com/mozilla/bidpom',
      packages=['bidpom', 'bidpom.pages'],
      include_package_data=True,
      install_requires=['PyPOM==1.1.1'],
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='mozilla browserid bidpom persona page object model selenium',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'])
