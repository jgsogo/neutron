#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Credit: http://stackoverflow.com/questions/3223604/how-to-create-a-temporary-directory-and-get-the-path-file-name-in-python

import contextlib
import os
import shutil
import tempfile


@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()


@contextlib.contextmanager
def tempdir():
    dirpath = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dirpath)
    with cd(dirpath, cleanup):
        yield dirpath


"""
# Usage example:
def main():
    with tempdir() as dirpath:
        pass # do something here
"""