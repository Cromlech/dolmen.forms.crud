# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '2.0a1dev'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.content >= 0.7.1',
    'dolmen.forms.base',
    'dolmen.forms.ztk',
    'grokcore.component',
    'martian',
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
    'zope.security',
    ]

tests_require = [
    'zope.annotation',
    'zope.i18n',
    'dolmen.location',
    ]

setup(name=name,
      version=version,
      description="CRUD forms and actions for `dolmen.content`",
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
