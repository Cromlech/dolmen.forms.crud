from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '0.4'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.content >= 0.2.2',
    'dolmen.forms.base >= 0.1',
    'grokcore.component',
    'megrok.pagetemplate >= 0.3',
    'megrok.z3cform.base >= 0.2',
    'setuptools',
    'zope.cachedescriptors',
    'zope.component >= 3.9.1',
    'zope.container',
    'zope.event',
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
    'megrok.layout',
    'zope.i18n',
    'zope.principalregistry',
    'zope.securitypolicy',
    'zope.site',
    'zope.testing',
    ]

setup(name = name,
      version = version,
      description = "Auto-generated forms for dolmen.content",
      long_description = readme + '\n\n' + history,
      keywords = 'Dolmen Grok Content Forms',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = '',
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
