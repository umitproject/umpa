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
import sys
import shutil
import tempfile

old_expanduser = os.path.expanduser

class TestUMPAInitialization(object):
    def setup_class(cls):
        # overwrite expanduser to use our temporary directory
        # NOTE: this test has to be run as a first because of this!
        def expanduser(path):
            return cls.tmp_dir
        cls.tmp_dir = tempfile.mkdtemp()
        #cls.old_expanduser = os.path.expanduser
        os.path.expanduser = expanduser
        import umpa
        # dirty hack to get possibility of reload module later
        globals()[umpa.__name__] = umpa

    def teardown_class(cls):
        shutil.rmtree(cls.tmp_dir)
        os.path.expanduser = old_expanduser

    def test_paths(self):
        def path_exist(path):
            assert os.path.isdir(path)
            assert os.path.isfile(os.path.join(path, '__init__.py'))

        home = os.path.join(os.path.expanduser('~'), '.umpa')
        dirs = ('umpa_plugins',
                os.path.join('umpa_plugins', 'protocols'),
                os.path.join('umpa_plugins', 'extensions'),
            )
        path_list = [ os.path.join(home, p) for p in dirs ]

        for path in path_list:
            yield path_exist, path

    def test_syspath(self):
        home = os.path.join(os.path.expanduser('~'), '.umpa')
        assert home in sys.path
        assert sys.path.index(home) == 0

    def test_reconstruct_broken_directory(self):
        home = os.path.join(os.path.expanduser('~'), '.umpa')
        for dir in os.listdir(home):
            shutil.rmtree(os.path.join(home,dir))
        reload(umpa)
        self.test_paths()
