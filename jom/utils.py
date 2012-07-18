'''
Copyright PuzzleDev s.n.c.
Created on Jul 14, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import os

def ensure_dir(filename):
    """ Creates the given folder if it does not exist.
    """
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
        