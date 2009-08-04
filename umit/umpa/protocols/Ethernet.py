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
Ethernet protocol implementation.
"""

import struct

from umit.umpa.protocols import _protocols
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _consts

__all__ = [ "Ethernet", ]

class _HType(_fields.SpecialIntField, _fields.EnumField):
    """
    The Type field indicates which protocol is encapsulated in upper layer.
    """
    bits = 16
    auto = True
    enumerable = {
        "ARP"   : _consts.ETHERTYPE_ARP,
        "RARP"  : _consts.ETHERTYPE_RARP,
        "IP"    : _consts.ETHERTYPE_IP,
        "IPv6"  : _consts.ETHERTYPE_IPV6,
        "PPPoE" : _consts.ETHERTYPE_PPPOE,
        }

    def _generate_value(self):
        """
        Generate value for undefined field yet.

        @return: auto-generated value of the field.
        """
        return self._tmp_value

class Ethernet(_protocols.Protocol):
    """
    Ethernet protocol implementation.

    The main protocol in second layer of OSI model.
    This is Ethernet Version 2 (so-called DIX frame).
    @note: This implemenation handles with MAC header in fact.
    CRC checksum field is untouched.
    """

    layer = 2       # layer of OSI
    protocol_id = _consts.DLT_EN10MB
    payload_fieldname = '_type'
    name = "Ethernet"

    _ordered_fields = ('dst', 'src', '_type')

    def __init__(self, **kwargs):
        fields_list = [ _fields.MACAddrField('Destination',
                                                        '00:00:00:00:00:00'),
                        _fields.MACAddrField('Source', '00:00:00:00:00:00'),
                        _HType('Type') ]

        super(Ethernet, self).__init__(fields_list, **kwargs)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        Set Padding field, calculate header and total length,
        set protocol of the upper layer.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        # Type
        # field indicates the next level type
        if self.payload:
            type_id = self.payload.protocol_id
        else:
            type_id = 0 # FIXME: what's the default value for non-upper layer?
        self.get_field('_type')._tmp_value = type_id

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields after calling fillout() for them.

        Calculate header checksum.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        return raw_value, bit

    def load_raw(self, buffer):
        """
        Load raw and update a protocol's fields.

        @return: raw payload
        """

        header_size = 14
        header_format = '!6B6BH'
        fields = struct.unpack(header_format, buffer[:header_size])

        self.dst = ':'.join(['%.2x'] * 6) % (fields[0:6])
        self.src = ':'.join(['%.2x'] * 6) % (fields[6:12])
        self._type = fields[12]

        return buffer[header_size:]

protocols = [ Ethernet, ]
