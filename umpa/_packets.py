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

"""
This module manages with packets.

Packet class is a protocol container.
Use it to build a packet which contains several protocols.
"""

import struct
import warnings

import umpa.utils.bits
from umpa.utils.exceptions import UMPAStrictException

BYTE = 8

class StrictWarning(Warning):
    """
    New category of warning.

    It's being used for warning message with reference
    to strict attribute of Packet's objects.
    """

    pass

def strict_warn(layer_a, layer_b):
    """
    Issue the warning with prepared message as a StrictWarning category.

    @type layer_a: C{int}
    @param layer_a: layer for first protocol.

    @type layer_b: C{int}
    @param layer_b: layer for second protocol.
    """

    msg = "bad protocols ordering. first layer %d, second %d." % (layer_a,
                                                                    layer_b)
    warnings.warn(msg, StrictWarning, stacklevel=3)

class Packet(object):
    """
    This is a protocol container.

    Use this to build a completely packets.
    An instance of the class should contains protocols which you want to send.
    """

    def __init__(self, *protos, **kwds):
        """
        Create a new Packet().

        @type *protos: Optional C{Protocol}
        @param *protos: protocols which will be included into the object.

        @type **kwds: Optional C{bool}
        @param **kwds: 2 keys are proper:
            -- strict (default True): if True object will keep protocols order.
            It avoids to build odd packets with with unsaved layer order
            -- warn (default True): if True and strict is True, object will
            issue warnings. Otherwise warnings are ignored.
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
        """
        Print in human-readable tree-style a content of the packet.

        It calls print statement for protocols.

        @return: call __str__ method of super-class.
        """

        print "Packet contains %d protocols" % len(self.protos)
        for proto in self.protos:
            print proto
        return super(Packet, self).__str__()

    def print_protocols(self):
        """
        Print all included protocols into the packet.
        """
        for p in self.protos:
            print p

    def include(self, *protos):
        """
        Add protocols into packet.

        @type *protos: C{Protocol}
        @param *protos: protocols which will be included into the packet.
        """

        self._add_new_protocols(protos)

    def _add_new_protocols(self, protos):
        """
        Add protocols into packet.

        Check the strict attribute and
        raise UMPAStrictException or issues warnings if needed.

        @type protos: C{Protocol}
        @param protos: protocols which will be included into the packet.
        """

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
        """
        Return raw packet in the bit-mode (big-endian).

        Call every protocols to get the raw bits of them,
        collect the results and return the raw packet.

        @return: Struct packed bits of every protocols in big-endian order.
        """

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
        """
        Return warn attribute.

        Warn attribute set a behaviour of strict attribute.
        If warn is True and strict is True, object will
        issue warnings if needed. Otherwise warnings are ignored.

        @return: warn attribute.
        """
        return self._warn

    def _setwarn(self, val):
        """
        Set warn attribute

        Warn attribute set a behaviour of strict attribute.
        If warn is True and strict is True, object will
        issue warnings if needed. Otherwise warnings are ignored.

        @type val: C{bool}
        @param val: bool value.
        """

        self._warn = val
        if self._warn:
            warnings.simplefilter('always', StrictWarning)
        else:
            warnings.simplefilter('ignore', StrictWarning)

    warn = property(_getwarn, _setwarn)
