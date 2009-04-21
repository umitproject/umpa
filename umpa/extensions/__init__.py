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
Global extensions which add extra usability / features.

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
import warnings

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
        msg = "Can't load the extension.\n" + repr(err) + "\n..ignoring."
        warnings.simplefilter('always', ImportWarning)
        warnings.warn(msg, ImportWarning)

def get_locals():
    """
    Return local extensions.

    Local extensions are the ones which are located in the user home directory.
    Usually it's $HOME/.umpa/umpa_plugins/extensions/.

    @rtype: C{list}
    @return: local extensions.
    """

    return _lextensions

def get_globals():
    """
    Return global extensions.

    Global extensions are the ones which are located
    in the umpa.extensions package.

    @rtype: C{list}
    @return: global extensions.
    """

    return _gextensions

def get_all():
    """
    Return all available extensions.

    Include global and local extensions.

    @rtype: C{list}
    @return: available extensions.
    """

    both = get_locals()[:]
    both.extend(get_globals())

    return both

def _list_local_extensions():
    """
    Scan for local extensions.

    Scan $HOME/.umpa/umpa_plugins/extensions directory.

    @rtype: C{list}
    @return: list of available extensions.
    """

    return [ ext[:-3] for ext
            in os.listdir(os.path.join(os.path.expanduser('~'), '.umpa',
                                            'umpa_plugins', 'extensions'))
            if ext.endswith('.py') and not ext.startswith('_') ]
    
_gextensions = [ "XML", "schedule" ]
_lextensions = _list_local_extensions()
