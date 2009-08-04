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

import os
import umit.umpa.extensions

class TestExtensionInit(object):
    def test_load_global(self):
        umit.umpa.extensions.load_extension('XML')
        assert umit.umpa.extensions.XML

        #umit.umpa.extensions.load_extension('route')
        #assert umit.umpa.extensions.route

    def test_load_local(self):
        for file in os.listdir(os.path.join(os.path.expanduser('~'),
                            '.umpa', 'umpa_plugins', 'extensions')):
            if file.startswith('_'):
                continue
            umit.umpa.extensions.load_extension(file[:-3])
            assert getattr(umit.umpa.extensions, file[:-3])
    
    def test_get_locals(self):
        for file in os.listdir(os.path.join(os.path.expanduser('~'),
                            '.umpa', 'umpa_plugins', 'extensions')):
            if file.startswith('_'):
                continue
            assert file[:-3] in umit.umpa.extensions.get_locals()
