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
import shutil
import tempfile

import umpa.extensions

old_expanduser = os.path.expanduser

class TestExtensionInit(object):
    def test_load_global(self):
        umpa.extensions.load_extension('XML')
        assert umpa.extensions.XML
    
class TestExtensionInitLocal(object):
    disabled = True
    def setup_class(cls):
        # this code is similar for tests/unit/test_0init.py
        def expanduser(path):
            return cls.tmp_dir

        cls.tmp_dir = tempfile.mkdtemp()
        os.path.expanduser = expanduser

    def teardown_class(cls):
        os.path.expanduser = old_expanduser
        shutil.rmtree(cls.tmp_dir)

    def test_load_local(self):
        def newpackage(path):
            print path
            os.makedirs(path)
            open(os.path.join(path, '__init__.py'), 'w').close()
            print os.listdir(path)

        local_path = os.path.join(os.path.expanduser('~'), '.umpa')
        newpackage(os.path.join(local_path, 'umpa_plugins'))
        newpackage(os.path.join(local_path, 'umpa_plugins', 'extensions'))

        open(os.path.join(local_path, 'umpa_plugins', 'extensions',
                                                            'foobar.py'), 'w')
        print os.listdir(os.path.join(local_path, "umpa_plugins/extensions"))
        umpa.extensions.load_extension('foobar')
        print local_path
        print dir(umpa.extensions)
        assert umpa.extensions.foobar
        

