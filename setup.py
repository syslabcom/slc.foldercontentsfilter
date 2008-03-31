from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='slc.foldercontentsfilter',
      version=version,
      description="A livesearch box for folder_contents to quickly find items in a large folder",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='livesearch folder_contents filter',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='https://svn.plone.org/svn/collective/slc.foldercontentsfilter',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['slc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
