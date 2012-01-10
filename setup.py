# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '2.0b1'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser >= 0.3a2',
    'dolmen.forms.base >= 2.0b2',
    'dolmen.forms.ztk >= 2.0b1',
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
    'cromlech.browser [test]',
    'cromlech.io [test]',
    'zope.configuration',
    ]

setup(name=name,
      version=version,
      description="CRUD forms and actions for Dolmen",
      long_description=u"%s\n\n%s" % (readme, history),
      keywords='Dolmen Grok Content Forms',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
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
