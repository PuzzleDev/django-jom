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
        JomFactory.autodiscover()
        factory = JomFactory.default()
        
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
        
        for model, jomDescriptor in factory.descriptors.items():
            # get the django module name
            app_name = model.__module__.split(".")[::-1][1]
            app_folder = os.path.join(folder, app_name).replace("\\","/")
            filename = os.path.join(app_folder, jomDescriptor.__class__.__name__ + ".js").replace("\\","/")
            ensure_dir(filename)
            print("[JOM] Generating " + filename)
            out_file = open(filename,"w")
            out_file.write(factory.getJomClass(model).renderClass())
            out_file.close()
        
            