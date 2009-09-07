from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='dolmen.forms.crud',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.forms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'grokcore.security',
          'grokcore.component',
          'dolmen.content',
          'megrok.z3cform',
          'zope.event',
          'zope.schema',
          'zope.location',
          'zope.security',
          'zope.component',
          'zope.interface',
          'zope.configuration',
          'zope.lifecycleevent',
          'zope.cachedescriptors',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
