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

def load_extension(name):
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
