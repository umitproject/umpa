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
This package contains several extensions.

Extensions may change behaviour of the library or add extra functionality.
In general, it's similar to plugins system.

There are 2 ways to load an extension:
 1. by load_extension() function for local and global extensions
    (e.g. C{umpa.extensions.load_extension("XML")}),
 2. by import statement
     - global example: C{import umpa.extensions.XML},
     - local example: C{import umpa_plugins.extensions.XML}

@note: Extensions have to be single .py files.
"""

import sys
import os.path

def load_extension(name):
    """
    Load the requested extension.

    First, I{locally} check the $HOME/.umpa location.
    If failure, I{globally} check the name in umpa.extensions package.
    """

    if os.path.isfile(os.path.join(os.path.expanduser('~'), '.umpa',
                            'umpa_plugins', 'extensions', name+'.py')):
        module_path = "umpa_plugins.extensions.%s" % name
    else:
        module_path = "umpa.extensions.%s" % name

    try:
        module = __import__(module_path, fromlist=[None])
        globals()[name] = module
    except Exception, err:
        print >> sys.stderr, "Can't load the extension."
        print >> sys.stderr, err
        print >> sys.stderr, "..ignoring."
