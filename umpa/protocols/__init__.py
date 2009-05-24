#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This library is free software; you can redistribute it and/or modify 
# it under the terms of the GNU Lesser General Public License as published 
# by the Free Software Foundation; either version 2.1 of the License, or 
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public 
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License 
# along with this library; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 

"""
Already implemented protocols and API to implement another.

Modules which names start with '_' prefix are for developers
and they are useful to implement new protocols.

Available protocols are in modules without '_' prefix.
"""

import sys
import os.path
import warnings

# loading global protocols
from IP import IP
# from ICMP import ICMP
from TCP import TCP
from UDP import UDP
from Payload import Payload

def get_locals():
    """
    Return local protocols.

    Local protocols are the ones which are located in the user home directory.
    Usually it's $HOME/.umpa/umpa_plugins/protocols/.

    @rtype: C{dict}
    @return: local protocols.
    """

    return _lproto

def get_globals():
    """
    Return global protocols.

    Global protocols are the ones which are located
    in the umpa.protocols package.

    @rtype: C{dict}
    @return: global protocols.
    """

    return _gproto

def get_all():
    """
    Return all available protocols.

    Include global and local protocols.

    @rtype: C{dict}
    @return: all protocols.
    """

    both = get_locals().copy()
    both.update(get_globals())

    return both

# loading local protocols (from $HOME/.umpa/umpa_plugins/protocols)
def _load_local_protocols():
    """
    Load local protocols.

    Load protocols from $HOME/.umpa/umpa_plugins/protocols directory.

    @rtype: C{list}
    @return: list of protocols' classes.
    """

    path = os.path.join(os.path.expanduser('~'), '.umpa', 'umpa_plugins',
                                                                'protocols')
    items = []
    for fname in os.listdir(path):
        if not fname.lower().endswith(".py") or fname.startswith("_"):
            continue

        try:
            module = __import__(
                    "umpa_plugins.protocols.%s"  % fname.replace(".py",""),
                    fromlist=[None])
            items.extend(module.protocols)
        except Exception, err:
            msg = "Can't load the extension.\n" + repr(err) + "\n..ignoring."
            warnings.simplefilter('always', ImportWarning)
            warnings.warn(msg, ImportWarning)
    return items

def _dict_protos(protos_list):
    """
    Create a dictionary from the protocol's list.

    Keys are names of protocols.
    Values are protocols' classes.

    @param protos_list: protocol's list

    @return: a dictionary of protocols' classes.
    """

    protos_dict = {}
    for proto in protos_list:
        protos_dict[proto.name] = proto
    return protos_dict

_gprotos_list = [ IP, TCP, UDP, Payload ]
_lprotos_list = _load_local_protocols()

_gproto = _dict_protos(_gprotos_list)
_lproto = _dict_protos(_lprotos_list)

# cleaning
del _gprotos_list
del _lprotos_list
