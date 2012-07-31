'''
Copyright PuzzleDev s.n.c.
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import os
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """ Delete all the Jom files
    """
    help = 'Delete all the jom files'

    def handle(self, *args, **options):
        
        # By default jom files are placed in MEDIA_ROOT
        # and not in STATIC_ROOT because only collectstatic
        # should put files in STATIC_ROOT
        base_path = settings.MEDIA_ROOT
        if hasattr(settings, 'JOM_ROOT'):
            # Developers can specify a different path by
            # setting the JOM_ROOT variable and adding it to
            # settings.STATICFILES_DIRS
            base_path = settings.JOM_ROOT
        folder = os.path.join(base_path, "jom/js/descriptors").replace("\\","/")
        shutil.rmtree(folder)
        