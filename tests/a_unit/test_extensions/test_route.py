#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: Luís A. Bastião Silva <luis.kop@gmail.com>
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


import py.test
import os
from umpa.extensions.route import Route

class TestExtensionRoute(object):
    def setup_class(cls):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-priviliges are needed')
        if os.name != 'posix':
            py.test.skip('only for POSIX platforms')
    def test_route_ipv4(self):
        def is_inside(dst,routes):
            found = False
            for i in routes:
                if i.get('dst')==dst:
                    found = True
                    break
            return found
        def get_route(dst, routes):
            route = None
            for i in routes:
                if i.get('dst')==dst:
                    route = i
                    break
            return route
        _dst = "127.0.2.0"
        _gw = "127.0.0.1"
        _mask = "255.255.255.0"
        r = Route()
        r.add(_dst, _mask, _gw)
        routes = r.get_routes()
        # Verify if entry is added
        assert is_inside(_dst, routes) == True
        #Verify Mask and Gateway:
        route = get_route(_dst, routes)
        assert route.get('gw') == _gw
        assert route.get('mask') == _mask
        r.delete(_dst)
        routes = r.get_routes()
        # Verify if entry was removed
        assert is_inside("192.168.2.0", routes) == False


    
    
    