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
        JomFactory.registerAll()
        factory = JomFactory.default()
        
        folder = os.path.join(settings.MEDIA_ROOT, "jom/").replace("\\","/")
        ensure_dir(folder)
        
        for jomClass in factory.entries:
            print("Writing " + jomClass.__name__)
            filename = os.path.join(folder, jomClass.__name__ + ".js").replace("\\","/")
            out_file = open(filename,"w")
            out_file.write(jomClass().renderClass())
            out_file.close()
        
            