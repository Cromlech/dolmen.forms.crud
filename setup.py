from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.crud'
version = '0.2'
readme = open(join('src', 'dolmen', 'forms', 'crud', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'setuptools',
    'grokcore.security',
    'grokcore.component',
    'grokcore.viewlet',
    'zope.event',
    'zope.schema',
    'zope.location',
    'zope.security',
    'zope.component',
    'zope.interface',
    'zope.publisher',
    'zope.traversing',
    'zope.lifecycleevent',
    'zope.cachedescriptors',
    'zope.app.container',
    'dolmen.field >= 0.3',
    'dolmen.content >= 0.2.2',
    'dolmen.forms.base >= 0.1',
    'megrok.pagetemplate >= 0.3',
    'megrok.z3cform.base >= 0.1',
    ]

tests_require = install_requires + [
    'zope.testing',
    'zope.securitypolicy',
    'zope.app.testing',
    'zope.app.zcmlfiles',
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
