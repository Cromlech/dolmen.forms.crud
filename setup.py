from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '1.0'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.content >= 0.7.1',
    'dolmen.forms.base >= 1.0b1',
    'grokcore.component',
    'martian',
    'setuptools',
    'zeam.form.base',
    'zeam.form.layout',
    'zeam.form.ztk',
    'zope.cachedescriptors',
    'zope.component >= 3.9.1',
    'zope.container',
    'zope.dublincore',
    'zope.event',
    'zope.i18n',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.lifecycleevent',
    'zope.location',
    'zope.publisher',
    'zope.schema',
    'zope.security',
    'zope.traversing',
    ]

tests_require = [
    'grokcore.message',
    'megrok.layout',
    'zope.annotation',
    'zope.i18n',
    'zope.principalregistry',
    'zope.securitypolicy',
    'zope.session',
    'zope.site',
    ]

setup(name = name,
      version = version,
      description = "CRUD forms and actions for `dolmen.content`",
      long_description = readme + '\n\n' + history,
      keywords = 'Dolmen Grok Content Forms',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://www.dolmen-project.org',
      license = 'GPL',
      packages = find_packages('src', exclude=['ez_setup']),
      package_dir = {'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.forms'],
      include_package_data = True,
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      test_suite = "dolmen.forms.crud",
      classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Zope3',
          'Intended Audience :: Other Audience',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      )
