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
      description = "",
      long_description = "",
      download_url = "",
      classifiers = [
                'Environment :: Web Environment',
                'Programming Language :: Python',
                ],
      platforms = [
                "Linux",
                ],
      license = "",
      packages = [
                'jom',
                'jom.management',
                'jom.management.commands',
                'jom.admin',
                ],
       package_data = {
                'jom': ['templates/*.*',
                        'templates/jom/*.*',
                        'templates/jom/templatetags/*.*'],
                }
     )