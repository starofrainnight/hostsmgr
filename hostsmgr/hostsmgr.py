# -*- coding: utf-8 -*-

"""Main module."""

import io
import os
import sys
import os.path
from .entry import from_string as entry_from_string
from .exceptions import *
from six import string_types


def guess_hosts_path():
    """Guess hosts path

    :raises HostsNotFound: If failed to find the hosts file
    :return: The hosts file path
    :rtype: str
    """

    # References to https://en.wikipedia.org/wiki/Hosts_(file)
    possible_paths = [
        # Unix, Unix-like, POSIX, Apple Macintosh Mac OS X 10.2 and newer,
        # Android, iOS 2.0 and newer
        '/etc/hosts',
        # Microsoft Windows NT, 2000, XP,[5] 2003, Vista, 2008, 7, 2012, 8, 10
        r'${SystemRoot}\System32\drivers\etc\hosts',
        # Microsoft Windows 95, 98, ME
        r'${WinDir}\hosts',
        # Microsoft Windows 3.1
        r'${WinDir}\HOSTS',
        # Symbian OS 6.1–9.0
        r'C:\system\data\hosts',
        # Symbian OS 9.1+
        r'C:\private\10000882\hosts',
        # Plan 9
        '/lib/ndb/hosts',
        # BeOS
        '/boot/beos/etc/hosts',
        # Haiku
        '/boot/common/settings/network/hosts',
    ]

    for path in possible_paths:
        path = os.path.expandvars(os.path.expanduser(path))
        if os.path.exists(path):
            return path

    # Meet unsupported OS
    raise HostsNotFound()


class HostsMgr(object):

    def __init__(self):
        self._entries = []

    def clear(self):
        self._entries.clear()

    def load(self, file):
        """Load hosts from file

        :param file: The opened file object (should open with read text
        mode) or str path to hosts file
        :param file: str or file object, optional
        """

        self.clear()

        hosts_file = file
        if isinstance(file, string_types):
            hosts_file = open(file, 'r')

        # Analyse hosts format
        try:
            for line in hosts_file.readlines():
                # There maybe \r, \n or both at the end of line.
                line = line.rstrip()
                self._entries.append(entry_from_string(line))
        finally:
            if isinstance(file, string_types):
                hosts_file.close()

    def loads(self, astr):
        self.load(io.StringIO(astr))

    def save(self, file):
        """Save hosts to file

        :param file: The opened file object (should open with write text mode)
        or str path to hosts file
        :param file: str or file object, optional
        """

        hosts_file = file
        if isinstance(file, string_types):
            hosts_file = open(file, 'w')

        try:
            hosts_file.writelines(
                [entry.expansion for entry in self._entries])
        finally:
            if isinstance(file, string_types):
                hosts_file.close()

    def saves(self):
        strio = io.StringIO()
        self.save(strio)
        return strio.getvalue()
