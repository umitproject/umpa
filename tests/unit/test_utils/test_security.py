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
import py.test
from umpa.utils.security import *

def foo():
    return 1

def bar(a):
    return a

class TestUtilSecurity(object):
    def setup_class(cls):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-priviliges are needed')

    def teardown_method(self, method):
        if os.name == 'posix':
            os.seteuid(0)

    def test_drop(self):
        import pwd
        drop_priviliges()
        assert os.geteuid() == pwd.getpwnam('nobody')[2]

    def test_drop_argument(self):
        drop_priviliges(1)
        assert os.geteuid() == 1

    def test_super_euid(self):
        euid = os.geteuid()
        super_priviliges(foo)
        assert euid == os.geteuid()

    def test_super_fun_call(self):
        result = super_priviliges(foo)
        assert result == 1

    def test_super_fun_call_arg(self):
        result = super_priviliges(bar, "foobar")
        assert result == "foobar"
