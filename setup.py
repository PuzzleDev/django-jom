'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''

#!/usr/bin/env python

from distutils.core import setup

setup(name = 'django-puzzledev-jom',
      version = '1.0',
      author = "Michele Sama",
      author_email = "m.sama@puzzledev.com",
      maintainer = "Michele Sama",
      maintainer_email = "m.sama@puzzledev.com",
      url = "www.puzzledev.com/",
      description = "Automatically extracts and keep synchronized Javascript objects from Django models",
      long_description = "django-jom is a Django/Javascript implementation of the SSMVC pattern. Interactive, rich and mobile web applications are based on the MVC pattern in which models contains the data on which the application is built. However mobile and Javascript clients are forced to replicate the MVC pattern in order to operate. The SSMVC pattern avoid code duplication by automatically extracting and synchronizing the front-end models with back-end.",
      download_url = "https://github.com/msama/django-jom",
      classifiers = [
                'Environment :: Web Environment',
                'Programming Language :: Python',
                ],
      platforms = [
                "Linux",
                ],
      license = "LGPL",
      packages = [
                'jom',
                'jom.management',
                'jom.management.commands',
                'jom.templatetags',
                ],
       package_data = {
                'jom': ['templates/*.*',
                        'templates/jom/*.*',
                        'templates/jom/templatetags/*.*',
                        'static/*.*',
                        'static/jom/*.*',
                        'static/jom/js/*.*'],
                }
     )