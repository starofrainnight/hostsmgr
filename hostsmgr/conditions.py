
"""A series conditions that use for search from a hosts table
"""

import ipaddress
from .entry import HostsEntry


class Condition(object):

    def __init__(self):
        pass

    def __call__(self, entry):
        raise NotImplementedError()

    def __and__(self, a, b):
        return And(a, b)

    def __or__(self, a, b):
        return Or(a, b)

    def __not__(self, obj):
        return Not(obj)


class Any(Condition):

    def __init__(self, *args):
        super().__init__()

        self._conds = args

    def __call__(self, entry):
        for cond in self._conds:
            if cond(entry):
                return True

        return False


class All(Condition):

    def __init__(self, *args):
        super().__init__()

        self._conds = args

    def __call__(self, entry):
        for cond in self._conds:
            if not cond(entry):
                return False

        return True


class Not(Condition):

    def __init__(self, cond):
        super().__init__()

        self._cond = cond

    def __call__(self, entry):
        return not cond(entry)


class And(All):
    pass


class Or(Any):
    pass


class HostsEntryFilter(Condition):

    def __call__(self, entry):
        return isinstance(entry, HostsEntry)


class IPAddress(HostsEntryFilter):

    def __init__(self, address):
        self._address = ipaddress.ip_address(address)

    def __call__(self, entry):
        if not super().__init__(entry):
            return False

        return self._address == entry.address


class Host(HostsEntryFilter):

    def __init__(self, host):
        self._host = host

    def __call__(self, entry):
        if not super().__init__(entry):
            return False

        return self._host in entry.hosts


class InLineComment(HostsEntryFilter):

    def __init__(self, value, case_sensitivity=True):
        self._value = value
        self._case_sensitivity = case_sensitivity

    def __call__(self, entry):
        if not super().__init__(entry):
            return False

        if self._case_sensitivity:
            return self._value == entry.comment
        else:
            return self._value.lower() == entry.comment.lower()
