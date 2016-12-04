#!/usr/bin/env python

import os
from subprocess import call

import logging
log = logging.getLogger(__name__)


def makemessages(dir):
    locale_dir = os.path.join(dir, 'locale')
    if os.path.exists(locale_dir):
        log.debug("\t\t + {}".format(locale_dir))
        call(['django-admin', 'makemessages', '--all'])


def deploy():
    log.info("== Deploy Neutron ==")
    log.info("\t- makemessages")
    for dir, subdir, files in os.walk(os.path.abspath(os.path.dirname(__file__))):
        for sdir in subdir:
            makemessages(os.path.join(dir, sdir))

    log.info("\t- compilemessages")
    call(['django-admin', 'compilemessages'])

    log.info("\t- collectstatic")
    call(['python', 'manage.py', 'collectstatic', '--noinput'])

    log.info("Ready to run server!")


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)

    deploy()
