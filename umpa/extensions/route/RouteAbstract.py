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


"""
The goal of this extension is support an abstraction to 
Routing tables
"""

class RouteAbstract:
    def __init__(self):
        pass
    def get_routes(self):
        pass
    def get_routes6(self):
        pass
    def add(self, dst, mask, gw, dev=''):
        pass
    def add6(self, dst, gw):
        pass
    def delete(self, dst):
        pass
    def delete6(self, dst):
        pass

 