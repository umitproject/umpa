#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
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

import umpa

def test_paths():
    def path_exist(path):
        assert os.path.isdir(path)

    home = os.path.join(os.path.expanduser('~'), '.umpa')
    dirs = ('umpa_plugins',
            os.path.join('umpa_plugins', 'protocols'),
            os.path.join('umpa_plugins', 'extensions'),
        )
    path_list = [ os.path.join(home, p) for p in dirs ]

    for path in path_list:
        yield path_exist, path

def test_syspath():
    home = os.path.join(os.path.expanduser('~'), '.umpa')
    assert home in sys.path
    assert sys.path.index(home) == 0
