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

def drop_priviliges():
    """Some functions require root-privilegies and after we done them,
    we don't really need this privilegies. So, we can simple leave them.
    It makes the application more safier.

    For example, to open a socket we need those privilegies
    
    It works only under UNIX. For other operation systems,
    this function doesn't do anything.
    """

    # checking if it's UNIX-family OS
    if os.name != 'posix':
        return

    import pwd
    nobody_id = pwd.getpwnam('nobody')[2]
    os.seteuid(nobody_id)

def super_priviliges(fun=None, *fargs):
    """
    Request for root-priviliges.
    We can pass function then after call the function we drop priviliges again.
    """

    if os.name != 'posix':
        return

    import pwd
    os.seteuid(0)
    if fun:
        result = fun(*fargs)
        drop_priviliges()
        return result
