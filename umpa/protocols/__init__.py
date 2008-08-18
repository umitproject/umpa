#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
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

import sys
import os.path

# loading global protocols
from IP import IP
# from ICMP import ICMP
from TCP import TCP
from UDP import UDP
from Payload import Payload

def _load_local_protocols():
    path = os.path.join(os.path.expanduser('~'), '.umpa', 'umpa_plugins',
                                                                'protocols')
    for fname in os.listdir(path):
        if not fname.lower().endswith(".py") or fname.startswith("_"):
            continue

        try:
            module = __import__(
                    "umpa_plugins.protocols.%s"  % fname.replace(".py",""),
                    fromlist=[None])

            for proto in module.protocols:
                globals()[proto.__name__] = proto
        except Exception, err:
            print >> sys.stderr, "Can't load local plugins."
            print >> sys.stderr, err
            print >> sys.stderr, "..ignoring."

# loading local protocols (from $HOME/.umpa/umpa_plugins/protocols)
_load_local_protocols()
