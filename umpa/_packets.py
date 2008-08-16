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

import struct
import warnings

import umpa.utils.bits
from umpa.utils.my_exceptions import UMPAStrictException

BYTE = 8

class StrictWarning(Warning):
    pass

def strict_warn(layer_a, layer_b):
    msg = "bad protocols ordering. first layer %d, second %d." % (layer_a,
                                                                    layer_b)
    warnings.warn(msg, StrictWarning, stacklevel=3)

class Packet(object):
    """You have to use this class to build a completely packets.
    An instance of the class should contains protocols which
    you want to send."""

    def __init__(self, *protos, **kwds):
        """You can include some protocols objects in construtor
        or use include() method later.
        """
        
        if 'strict' in kwds:
            self.strict = kwds['strict']
        else:
            self.strict = True      # default value
            
        if 'warn' in kwds:
            self.warn = kwds['warn']
        else:
            self.warn = True        # default value

        self.protos = []
        self._add_new_protocols(protos)
        self.raw = None
        self.bits = 0

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

    def _add_new_protocols(self, protos):
        for p in protos:
            if len(self.protos) > 0:
                last_proto = self.protos[-1]
                if p.layer - last_proto.layer != 1: # FIXME: should allow only this?
                    if self.strict:
                        raise UMPAStrictException("bad protocols ordering. \
first layer %d, second %d." % (last_proto.layer, p.layer))
                    else:
                        strict_warn(last_proto.layer, p.layer)
                last_proto.__dict__['payload'] = p
            self.protos.append(p)

    def get_raw(self):
        """Return raw packet, in bit-mode (big-endian)."""

        self.raw = 0
        self.bits = 0
        proto_id = 0
        for proto in reversed(self.protos):
            # unfortunately we must pass list of protocols to every protocol
            # because some fields handle with other protocols, so they need
            # an access to them
            raw_proto, bit_proto = proto._get_raw(tuple(self.protos),
                                                                    self.bits)
            self.raw |= raw_proto << self.bits
            self.bits += bit_proto
        # split into chunks
        # we make it because we need string for socket object
        # so after that we pack it by struct module.pack()
        byte_chunks = umpa.utils.bits.split_into_chunks(self.raw, self.bits)
        return struct.pack('!' + 'B'*(self.bits/BYTE), *byte_chunks)

    def _getwarn(self):
        return self._warn

    def _setwarn(self, val):
        self._warn = val
        if self._warn:
            warnings.simplefilter('always', StrictWarning)
        else:
            warnings.simplefilter('ignore', StrictWarning)

    warn = property(_getwarn, _setwarn)
