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
Functions related with security issues.
"""

import os
import sys

def drop_priviliges(euid=None):
    """
    Change EUID of the current process to nobody.

    Some functions require root-privilegies and after we done them,
    we don't really need this privilegies. So, we can simple leave them.
    It makes the application more safier.

    For example, to open a socket we need those privilegies.
    
    It works only under UNIX. For other operation systems,
    this function doesn't do anything.

    @type euid: C{int}
    @param euid: UID number candidate (default: nobody)
    """

    # checking if it's UNIX-family OS
    if os.name != 'posix':
        return

    if euid is None:
        import pwd
        euid = pwd.getpwnam('nobody')[2]
    try:
        os.seteuid(euid)
    except OSError:
        print >> sys.stderr, "Run the program with root-priviliges.\n"
        raise
        
def super_priviliges(fun=None, *fargs, **kwargs):
    """
    Change EUID of the current process to 0 (root).

    Request for root-priviliges.
    Pass function, then after call the function, drop the priviliges again.

    @type fun: C{function}
    @param fun: function which will be called with EUID=0.

    @param fargs: arguments for the function.

    @param kwargs: key-arguments for the function.

    @return: if function is passed, return the result of the function
    """

    if os.name != 'posix':
        return

    old_euid = os.geteuid()
    try:
        os.seteuid(0)
    except OSError:
        print >> sys.stderr, "Run the program with root-priviliges.\n"
        raise
    if fun:
        result = fun(*fargs, **kwargs)
        drop_priviliges(old_euid)
        return result
