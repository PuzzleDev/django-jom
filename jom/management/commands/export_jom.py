'''
Copyright PuzzleDev s.n.c.
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from jom.factory import JomFactory
from jom.utils import ensure_dir


class Command(BaseCommand):
    """ Generate all the Jom files
    """
    help = 'Removes all the uploaded files which are not saved in the database'

    def handle(self, *args, **options):
        factory = JomFactory.default()
        
        apps = settings.INSTALLED_APPS
        for app in apps:
            try:
                print (app + ".joms")
                #import all the JOM classes
                __import__(app + ".joms", globals={}, locals={}, fromlist=[], level=-1)
            except ImportError:
                pass
            
        folder = os.path.join(settings.MEDIA_ROOT, "jom/").replace("\\","/")
        ensure_dir(folder)
        
        for entry in factory.entries:
            filename = os.path.join(folder, entry.model + ".js").replace("\\","/")
            out_file = open(filename,"w")
            out_file.write(entry.renderClass())
            out_file.close()
        
            