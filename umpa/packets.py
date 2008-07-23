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

class Packet(object):
    """You have to use this class to build a completely packets.
    An instance of the class should contains protocols which
    you want to send."""

    def __init__(self, *protos):
        """You can include some protocols objects in construtor
        or use include() method later.
        """
        self.protos = []
        self._add_new_protocols(protos)

    def __str__(self):
        """Print in human-readable style a content of the packet."""
        print "Not implemented yet."

    def print_protocols(self):
        """Print all included protocols into the packet."""
        for p in self.protos:
            print p

    def include(self, *protos):
        """Add protocols into packet.
        """
        self._add_new_protocols(protos)

    def _add_new_protocols(self, *protos):
        for p in protos:
            self.protos.append(p)

    def get_raw(self):
        """Return raw packet, in bit-mode (big-endian)."""
        # TODO: calling method to pack it for each protocols
        print "Not implemented yet."
