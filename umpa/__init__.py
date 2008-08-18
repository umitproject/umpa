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

import os
import sys

from _packets import Packet
from _sockets import Socket

local_path = os.path.join(os.path.expanduser('~'), '.umpa')
# checking if local directory exists
if not os.path.isdir(local_path):
    os.makedirs(os.path.join(local_path,'umpa_plugins','protocols'))
    os.mkdir(os.path.join(local_path,'umpa_plugins','extensions'))

sys.path.append(local_path)
del local_path
