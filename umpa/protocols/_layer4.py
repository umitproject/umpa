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

from umpa.protocols._protocols import Protocol
from umpa.protocols.IP import IP
from umpa.protocols._fields import *

class PortField(IntField):
    bits = 16
    auto = False

class Layer4ChecksumField(IntField):
    bits = 16
    auto = True
    def _generate_value(self):
        return 0

class PseudoHeader(Protocol):
    """This is class is useful for some protocols like TCP or UDP.
    It has been used to calculate checksum of those protocols.
    It's prefixed to the protocol header before calculating.
    """
    _ordered_fields = ('source_address', 'destination_address', 'reserved',
                    'protocol_id', 'total_length')

    def __init__(self, protocol_id, total_length):

        fields_list = [ IPv4AddrField("Source Address"),
                        IPv4AddrField("Destination Address"),
                        IntField("Reserved", 0, bits=8),
                        IntField("Protocol", protocol_id, bits=8),
                        IntField("Total Length", total_length, bits=16) ]
        super(PseudoHeader, self).__init__(fields_list)

    def _raw(self, protocol_container, protocol_bits):
        bit = 0
        raw_value = 0

        # grabbing informations from IP's header
        it = iter(protocol_container)
        for proto in it:
            if isinstance(proto,IP):
                break
        self.source_address = proto.source_address
        self.destination_address = proto.destination_address

        # so we make a big number with bits of every fields of the protocol
        for field in reversed(self._ordered_fields):
            x = self._get_field(field).fillout()
            raw_value |= x << bit
            bit += self._get_field(field).bits

        return raw_value, bit

