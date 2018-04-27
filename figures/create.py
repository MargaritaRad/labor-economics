#!/usr/bin/env python

"""This module creates all available figures and then provides them in a
compiled document for review.

"""

import subprocess
import shutil
import os

if __name__ == '__main__':

    for dirname in ['code', 'note']:
        os.chdir(dirname)
        subprocess.check_call(['python', './create.py'])
        os.chdir('../')

    shutil.copy('note/main.pdf', 'figures.pdf')
