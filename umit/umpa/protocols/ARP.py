#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
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
ARP (Address Resolution Protocol) protocol implementation.
"""

import struct

from umit.umpa.protocols import _consts
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _protocols

__all__ = [ "ARP", ]

class _HHWType(_fields.IntField):
    bits = 16
    auto = True

    def _generate_value(self):
        return 0x1 # Ethernet type

class _HProtoType(_fields.EnumField):
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
        return _consts.ETHERTYPE_IP

class _HHWSize(_fields.SpecialIntField):
    bits = 8
    auto = True

    def _generate_value(self):
        if self._tmp_value == 0x1:
            return 6
        else:
            return 0

class _HProtoSize(_fields.SpecialIntField):
    bits = 8
    auto = True

    def _generate_value(self):
        if self._tmp_value == _consts.ETHERTYPE_IP:
            return 4
        else:
            return 0

class _HOpcode(_fields.EnumField):
    bits = 16
    auto = False
    enumerable = {
        "REQUEST" : 0x1,
        "REPLY" : 0x2,
        }

# main ARP class

class ARP(_protocols.Protocol):
    """
    Address Resolution Protocol implementation.

    The protocol is the method for finding a host's link layer (hardware)
    address when only its Internet Layer (IP) or some other Network Layer
    address is known. ARP is defined in RFC 826.
    """

    layer = 3       # layer of OSI
    protocol_id = _consts.ETHERTYPE_ARP
    payload_fieldname = None
    name = "ARP"

    _ordered_fields = ('hwtype', 'prototype', '_hwsize', '_protosize',
                    'opcode', 'srchw_mac', 'srcproto_ipv4', 'dsthw_mac',
                    'dstproto_ipv4',)

    def __init__(self, **kwargs):
        """
        Create a new ARP().
        """

        fields_list = [ _HHWType("Hardware Type"),
                        _HProtoType("Protocol Type"),
                        _HHWSize("Hardware Size"),
                        _HProtoSize("Protocol Size"),
                        _HOpcode("Opcode"),
                        _fields.MACAddrField("Sender MAC Address",
                                            "00:00:00:00:00:00"),
                        _fields.IPv4AddrField("Sender IP Address",
                                            "127.0.0.1"),
                        _fields.MACAddrField("Target MAC Address",
                                            "00:00:00:00:00:00"),
                        _fields.IPv4AddrField("Target IP Address",
                                            "127.0.0.1"),
                ]

        # call super.__init__ after prepared necessary data
        super(ARP, self).__init__(fields_list, **kwargs)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self.get_field('srchw_mac').set_doc("Sender MAC address. "
                                        "See RFC 826 for more.")
        self.get_field('srcproto_ipv4').set_doc("Sender IP address. "
                                            "See RFC 826 for more.")
        self.get_field('dsthw_mac').set_doc("Target MAC address. "
                                        "See RFC 826 for more.")
        self.get_field('dstproto_ipv4').set_doc("Target IP address. "
                                            "See RFC 826 for more.")

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

        self.get_field('_hwsize')._tmp_value = \
            self.get_field('hwtype').fillout()
        self.get_field('_protosize')._tmp_value = \
            self.get_field('prototype').fillout()

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

        @return: raw payload (shouldn't nothing).
        """

        header_size = 28
        header_format = '!HHHH6B4B6B4B'
        fields = struct.unpack(header_format, buffer[:header_size])

        self.hwtype = fields[0]
        self.prototype = fields[1]
        self._hwsize = fields[2] >> 4
        self._protosize = fields[2] & 0x0f
        self.opcode = fields[3]
        self.srchw_mac = ':'.join(['%.2x']*6) % (fields[4:10])
        self.srcproto_ipv4 = '%d.%d.%d.%d' % (fields[10:14])
        self.dsthw_mac = ':'.join(['%.2x']*6) % (fields[14:20])
        self.dstproto_ipv4 = '%d.%d.%d.%d' % (fields[20:24])

        return buffer[header_size:]

protocols = [ ARP, ]
