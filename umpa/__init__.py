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

"""
UMPA - Umit's Manipulations of Packets Art

This is a packet manipulations library.
Packet manipulation library aims to provide easy to use system
to manipulate packets of every OSI model layers.

Available packages:
    - protocols
    - extensions
    - utils

For more information check docs/*
and official website U{http://umpa.umitproject.org}
"""

import os
import sys

from _packets import Packet
from _sockets import Socket

# UMPA handles with the local directory $HOME/.umpa
# especially with the $HOME/,umpa/umpa_plugins
# it's something similar to plugin system
# and we can easily import local protocols/extensions
local_path = os.path.join(os.path.expanduser('~'), '.umpa')

# checking if local directory exists
if not os.path.isdir(local_path):
    os.makedirs(os.path.join(local_path,'umpa_plugins','protocols'))
    os.mkdir(os.path.join(local_path,'umpa_plugins','extensions'))

# to allow things like: from umpa_plugins.extensions import something
# we need to add the local_path to the PYTHONPATH
sys.path.insert(0,local_path)

# delete unnecessary vars
del local_path
