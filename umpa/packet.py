#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

class Packet:
    '''You have to use this class to build a completely packets.
    An instance of the class should contains protocols which
    you want to send.'''

    def _add_new_protocols(*protos):
        for p in protos:
            self.protos.append(p)

    def __init__(self, *protos):
        '''You can include some protocols objects in construtor
        or use include() method later.
        '''
        self.protos = []
        self._add_new_protocols(protos)

    def include(self, *protos):
        '''You can add protocols into your packet.
        '''
        self._add_new_protocols(protos)
    def __str__(self):
        '''Prints in human-readable style a content of the packet.'''
        pass
    def print_protocols(self):
        '''Prints all included protocols into the packet.'''
        for p in self.protos:
            print p
