#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
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
Packets management.

Packet class is a protocol container.
Use it to build a packet which contains several protocols.
"""

import struct
import warnings

import umit.umpa.utils.bits
from umit.umpa.utils.exceptions import UMPAException, UMPAStrictException

BYTE = 8

class StrictWarning(Warning):
    """
    New category of warning.

    It's being used for warning message with reference
    to strict attribute of Packet's objects.
    """

    pass

def _strict_warn(layer_a, layer_b):
    """
    Issue the warning with prepared message as a StrictWarning category.

    @type layer_a: C{int}
    @param layer_a: layer for first protocol.

    @type layer_b: C{int}
    @param layer_b: layer for second protocol.
    """

    msg = "bad protocols ordering. first layer %d, then %d." % (layer_a,
                                                                layer_b)
    warnings.warn(msg, StrictWarning, stacklevel=3)

class Packet(object):
    """
    This is a protocol container.

    Use this to build a completely packets.
    An instance of the class should contains protocols which you want to send.
    """

    def __init__(self, *protos, **options):
        """
        Create a new Packet().

        @type protos: Optional C{Protocol}
        @param protos: protocols which will be included into the object.

        @type options: Optional C{bool}
        @param options: 2 keys are proper:
            - strict (default: True): if True object will keep protocols order.
            It avoids to build odd packets with with unsaved layer order
            - warn (default: True): if True and strict is True, object will
            issue warnings. Otherwise warnings are ignored.
        """
        
        # parsing options dictionary
        available_options = { 'strict' : True, 'warn' : True }
        for opt in available_options:
            if opt in options:
                setattr(self, opt, options[opt])
                options.pop(opt)
            else:
                setattr(self, opt, available_options[opt])
        if len(options) != 0:
            raise UMPAException("Undefined options " + str(options.keys()))

        self.protos = []
        self._add_new_protocols(protos)
        self.raw = None
        self.bits = 0

    def __getattr__(self, name):
        """
        Return the protocol with the name

        @type name: C{str}
        @param name: name of the protocol
        
        @return: protocol object
        """

        for proto in self.protos:
            if proto.name.lower() == name.lower():
                return proto
        raise AttributeError(name)

    def __str__(self):
        """
        Print in human-readable tree-style a content of the packet.

        Call print statement for protocols.

        @return: call __str__ method of super-class.
        """

        print "Packet contains %d protocols" % len(self.protos)
        for proto in self.protos:
            print proto
        return super(Packet, self).__str__()

    def include(self, *protos):
        """
        Add protocols into packet.

        @type protos: C{Protocol}
        @param protos: protocols which will be included into the packet.
        """

        self._add_new_protocols(protos)

    def _add_new_protocols(self, protos):
        """
        Add protocols into packet.

        Check the strict attribute and
        raise UMPAStrictException or issues warnings if needed.

        @param protos: protocols which will be included into the packet.
        """

        for proto in protos:
            if len(self.protos) > 0:
                last_proto = self.protos[-1]
                # XXX: should we allow only the distance no less and
                # no more than 1 between layers?
                if proto.layer - last_proto.layer != 1: 
                    if self.strict:
                        raise UMPAStrictException("bad protocols ordering. "
                            "first layer %d, second %d."
                            % (last_proto.layer, proto.layer))
                    else:
                        _strict_warn(last_proto.layer, proto.layer)
                last_proto.__dict__['payload'] = proto
            self.protos.append(proto)

    def get_raw(self):
        """
        Return raw packet in the bit-mode (big-endian).

        Call every protocols to get the raw bits of them,
        collect the results and return the raw packet.

        @return: Struct packed bits of every protocols in big-endian order.
        """

        self.raw = 0
        self.bits = 0
        for proto in reversed(self.protos):
            # unfortunately we must pass list of protocols to every protocol
            # because some fields handle with other protocols, so they need
            # an access to them
            raw_proto, bit_proto = proto.get_raw(tuple(self.protos), self.bits)
            self.raw |= raw_proto << self.bits
            self.bits += bit_proto
        # split into chunks
        # we make it because we need string for socket object
        # so after that we pack it by struct module.pack()
        byte_chunks = umit.umpa.utils.bits.split_number_into_chunks(
                                        self.raw, chunk_amount=self.bits/BYTE)
        return struct.pack('!' + 'B'*(self.bits/BYTE), *byte_chunks)

    def _getwarn(self):
        """
        Return warn attribute.

        Warn attribute set a behaviour of strict attribute.
        If warn is True and strict is True, object will
        issue warnings if needed. Otherwise warnings are ignored.

        @returns: warn attribute.
        """
        return self._warn

    def _setwarn(self, value):
        """
        Set warn attribute

        Warn attribute set a behaviour of strict attribute.
        If warn is True and strict is True, object will
        issue warnings if needed. Otherwise warnings are ignored.

        @type value: C{bool}
        @param value: bool value.
        """

        self._warn = value
        if self._warn:
            warnings.simplefilter('always', StrictWarning)
        else:
            warnings.simplefilter('ignore', StrictWarning)

    warn = property(_getwarn, _setwarn, doc="""
    Control if issue warnings or ignore them
    @type: C{bool}
    """)
