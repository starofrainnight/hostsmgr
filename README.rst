============================
hostsmgr (Hosts Manager)
============================


.. image:: https://img.shields.io/pypi/v/hostsmgr.svg
        :target: https://pypi.python.org/pypi/hostsmgr

.. image:: https://img.shields.io/travis/starofrainnight/hostsmgr.svg
        :target: https://travis-ci.org/starofrainnight/hostsmgr

.. image:: https://ci.appveyor.com/api/projects/status/lx6dwcisa6bolsqw?svg=true
        :target: https://ci.appveyor.com/project/starofrainnight/hostsmgr

.. image:: https://readthedocs.org/projects/hostsmgr/badge/?version=latest
        :target: https://hostsmgr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/starofrainnight/hostsmgr/shield.svg
     :target: https://pyup.io/repos/github/starofrainnight/hostsmgr/
     :alt: Updates


API for manage hosts file


* Free software: Apache-2.0
* Documentation: https://hostsmgr.readthedocs.io.


Features
--------

Usage
--------

.. code:: python

    from hostsmgr import HostsMgr
    from hostsmgr.hostsmgr import guess_hosts_path
    from hostsmgr.conditions import Any, All, IPAddress, Host, InlineComment

    mgr = HostsMgr()

    # Load system hosts file
    mgr.load(guess_hosts_path())

    # Save hosts to another place (Must open with text mode !)
    mgr.save(open('/etc/hosts.old', 'w'))

    # Save hosts to string with hosts file format
    hosts_string = mgr.saves()

    # Find all hosts entries that with 127.0.0.1 address
    entries = mgr.find(IPAddress('127.0.0.1'))

    # Find all entries that contained specific host
    entries = mgr.find(Host('localhost'))

    # Find all entries that contained specificed ip address and host both
    entries = mgr.find(IPAddress('127.0.0.1') & Host('localhost'))

    # Find all entries that contained either hosts
    entries = mgr.find(Host('ip6-localhost') | Host('localhost'))

    # Find all entries that contained either hosts, another method
    entries = mgr.find(Any(Host('ip6-localhost'), Host('localhost')))

    # Find all entries that contained both hosts
    entries = mgr.find(Host('ip6-localhost') & Host('localhost'))

    # Find all entries that contained both hosts, another method
    entries = mgr.find(All(Host('ip6-localhost'), Host('localhost')))

    # Find all entries that contained target inline comment
    entries = mgr.find(InlineComment('THIS_IS_A_TAG'))

    # Find only one entry that contained target inline comment
    entries = mgr.find(InlineComment('THIS_IS_A_TAG'), at_most=1)

    # Remove an entry that found by find()
    mgr.remove(entry)

    # Remove all hosts from hosts entries
    mgr.remove_by_hosts(['localhost', 'ip6-localhost'])

    # Remove all entries by inline comment exactly matched
    mgr.remove_by_inline_comment(InlineComment('TAG_FOR_EXAMPLE'))

    # Remove all entries by inline comment partial matched
    mgr.remove_by_inline_comment(InlineComment('TAG_FOR_EXAMPLE', partial=True))

Credits
---------

This package was created with Cookiecutter_ and the `PyPackageTemplate`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`PyPackageTemplate`: https://github.com/starofrainnight/rtpl-pypackage

