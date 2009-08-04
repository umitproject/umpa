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
Linux cooked-mode capture (SLL) protocol implementation.
"""
# for more information - see http://wiki.wireshark.org/SLL

import struct

from umit.umpa.protocols import _protocols
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _consts

__all__ = [ "SLL", ]

# TODO: some fields should have better implementation of generate_value()
# anyway the question is if we can try to send it. propably not

class _HPacketType(_fields.IntField):
    bits = 16
    auto = True

    def _generate_value(self):
        return 0

class _HHeaderAddressType(_fields.IntField):
    bits = 16
    auto = True

    def _generate_value(self):
        return 0

class _HHeaderAddressLength(_fields.IntField):
    bits = 16
    auto = True

    def _generate_value(self):
        return 0

class _HBlank(_fields.IntField):
    bits = 16
    auto = True

    def _generate_value(self):
        return 0

class _HProtocol(_fields.SpecialIntField, _fields.EnumField):
    """
    The Protocol field indicates which protocol is encapsulated in upper layer.
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

class SLL(_protocols.Protocol):
    """
    Linux cooked-mode capture (SLL) protocol implementation.

    This is the pseudo-protocol used by libpcap on Linux to capture
    from the "any" device and to capture on some devices where the native
    link layer header isn't available or can't be used.
    """

    layer = 2   # layer of OSI
    protocol_id = _consts.DLT_LINUX_SLL
    payload_fieldname = '_etype'
    name = "SLL"

    _ordered_fields = ('_pkttype', '_hatype', '_halen',
                        'src', '_blank', '_etype')

    def __init__(self, **kwargs):
        fields_list = [ _HPacketType("Packet Type"),
                        _HHeaderAddressType("Header Address Type"),
                        _HHeaderAddressLength("Header Address Length"),
                        _fields.MACAddrField("Source", "00:00:00:00:00:00"),
                        _HBlank("Blank"),
                        _HProtocol("Protocol") ]

        super(SLL, self).__init__(fields_list, **kwargs)

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
        self.get_field('_etype')._tmp_value = type_id

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

        header_size = 16
        header_format = '!HHH6BHH'
        fields = struct.unpack(header_format, buffer[:header_size])

        self._pkttype = fields[0]
        self._hatype = fields[1]
        self._halen = fields[2]
        self.src = ':'.join(['%.2x'] * 6) % (fields[3:9])
        self._blank = fields[9]
        self._etype = fields[10]

        return buffer[header_size:]

protocols = [ SLL, ]
