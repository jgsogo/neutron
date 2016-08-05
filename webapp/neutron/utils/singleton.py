#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import tempfile
import logging
from contextlib import contextmanager

log = logging.getLogger(__name__)


class SingleInstanceException(BaseException):
    pass


@contextmanager
def singleton(flavor_id=""):
    """
    Inspired by tendo.singleton: https://github.com/pycontribs/tendo/blob/master/tendo/singleton.py
    """
    basename = os.path.splitext(os.path.abspath(sys.argv[0]))[0].replace("/", "-").replace(":", "").replace("\\", "-") + '-{}.lock'.format(flavor_id)
    lockfile = os.path.normpath(os.path.join(tempfile.gettempdir(), basename))

    log.debug("singleton lockfile: " + lockfile)

    if sys.platform == 'win32':
        try:
            # file already exists, we try to remove (in case previous execution was interrupted)
            if os.path.exists(lockfile):
                os.unlink(lockfile)
            fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        except OSError:
            type, e, tb = sys.exc_info()
            if e.errno == 13:
                log.error("Another instance is already running, quitting.")
                raise SingleInstanceException()
            log.error("Unexpected error: [{}] {}".format(e.errno, e))
            raise
    else:  # non Windows
        import fcntl
        fp = open(lockfile, 'w')
        fp.flush()
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            log.warning("Another instance is already running, quitting.")
            raise SingleInstanceException()

    yield  # Return to main application flow

    try:
        if sys.platform == 'win32':
            os.close(fd)
            os.unlink(lockfile)
        else:
            import fcntl
            fcntl.lockf(fp, fcntl.LOCK_UN)
            # os.close(self.fp)
            if os.path.isfile(lockfile):
                os.unlink(lockfile)
    except Exception as e:
        log.error(e)
        raise
