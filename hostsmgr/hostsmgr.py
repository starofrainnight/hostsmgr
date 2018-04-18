# -*- coding: utf-8 -*-

"""Main module."""

import io
import os
import sys
import os.path
from .entries import HostsEntry
from .entries import from_string as entry_from_string
from .exceptions import *
from .conditions import Any, All, IPAddress, Host
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
        :type file: str or file object, optional
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
        :type file: str or file object, optional
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

    def find(self, condition, at_most=0):
        """Find entries by provided condition

        :param condition: The entries must match this condition
        :type condition: conditions.Condition
        :param at_most: How much we will stop finding at most, defaults to 0
        means unlimited.
        :type at_most: int, optional
        :return: A list of founded entries
        :rtype: list
        """

        if isinstance(condition, list):
            condition = All(*condition)

        found_entries = []

        for entry in self._entries:
            if not condition(entry):
                continue

            found_entries.append(entry)
            if (at_most >= 1) and (len(found_entries) >= at_most):
                break

        return found_entries

    def check(self, condition):
        """Check if there have any entry matched with provided condition

        :param condition: The condition need to check for
        :type condition: conditions.Condition
        :return: True if condition matched. Otherwise return False.
        :rtype: bool
        """

        return bool(self.find(condition, at_most=1))

    def add(self, hosts_entry):
        """Append the hosts entry to the end of hosts table

        :param hosts_entry: The new hosts entry which want to append the hosts
        :type hosts_entry: HostsEntry
        :raises ValueError: If there have any host same with one of hosts_entry
        host item.
        """

        if not hosts_entry.hosts:
            raise ValueError("HostsEntry's hosts must not empty!")

        matched = self.find(
            IPAddress(hosts_entry.address) & Any(
                *[Host(h) for h in hosts_entry.hosts]))

        if matched:
            matched_hosts = []
            for entry in matched:
                matched_hosts += entry.hosts

            raise ValueError(
                'These hosts exists already : %s' % matched_hosts)

        # There nothing same with us, append one
        self._entries.append(hosts_entry)

    def remove_by_hosts(self, hosts):
        matched = self.find(Any(*[Host(h) for h in hosts_entry.hosts]))
        for entry in matched:
            for host in hosts:
                entry.hosts.remove(host)

            # Remove the whole entry if hosts entry don't have any hosts
            if len(entry.hosts) <= 0:
                self._entries.remove(entry)
