#!/usr/bin/env python
"""This script creates and updates the tutorial files."""
import subprocess as sp
import argparse
import shutil
import glob
import os


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Create material for tutorial session')

    parser.add_argument('-u', '--update', action='store_true', dest='update',
                        help='update public material')

    is_update = parser.parse_args().update

    os.chdir('figures')
    for fname in glob.glob('*.py'):
        sp.check_call(['python', fname])
    os.chdir('../')

    for task in ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']:
        sp.check_call(task + ' main', shell=True)

    if is_update:
        shutil.move('main.pdf', '../distribution/tutorial_session.pdf')