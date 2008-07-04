#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import pwd

def leave_priviliges():
    '''Some functions require root-privilegies and after we done them,
    we don't really need this privilegies. So, we can simple leave them.
    It makes the application more safier.

    For example, to open a socket we need those privilegies
    
    It works only under UNIX. For other operation systems,
    this function doesn't do anything.
    '''

    # checking if it's UNIX-family OS
    if os.name != 'posix':
        return

    nobody_id = pwd.getpwnam('nobody')[2]
    os.seteuid(nobody_id)
