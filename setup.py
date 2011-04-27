# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '2.0a1dev'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.forms.base >= 2.0a1dev',
    'dolmen.forms.ztk >= 2.0a1dev',
    'dolmen.location',
    'grokcore.component',
    'setuptools',
    'zope.cachedescriptors',
    'zope.component',
    'zope.dublincore',
    'zope.event',
    'zope.i18n',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.lifecycleevent',
    'zope.location',
    'zope.schema',
    ]

tests_require = [
    'cromlech.io',
    'cromlech.webob',
    'zope.configuration',
    ]

setup(name=name,
      version=version,
      description="CRUD forms and actions for Dolmen",
      long_description=readme + '\n\n' + history,
      keywords='Dolmen Grok Content Forms',
      author='The Dolmen Team',
      author_email='trollfot@gmail.com',
      url='http://www.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.forms'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      test_suite="dolmen.forms.crud",
      classifiers=[
          'Environment :: Web Environment',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      )
