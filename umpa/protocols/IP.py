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

import umpa.protocols._consts as const

from umpa.protocols import *
from umpa.utils import net

class HVersion(IntField):
    """The Version field indicates the format of the internet header.
    
    See RFC 791 for more.
    """
    bits = 4
    auto = True
    def _generate_value(self):
        return const.IPVERSION_4

class HIHL(SpecialIntField):
    """Internet Header Length is the length of the internet header in 32 bit
    words, and thus points to the beginning of the data.
    
    See RFC 791 for more.
    """
    bits = 4
    auto = True
    def _generate_value(self):
        return 5 + self._tmp_value / 32 # 5 is a minimum value (see RFC 791)

class HTotalLength(SpecialIntField):
    """Total Length is the length of the datagram, measured in octets,
    including internet header and data.

    See RFC 791 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        return self._tmp_value / const.BYTE

class HIdentification(IntField):
    """An identifying value assigned by the sender to aid in assembling the
    fragments of a datagram.

    See RFC 791 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # TODO: implementation of fragmentation
        # otherwise we can simple return 0 ;-)
        return 0

class HFragmentOffset(IntField):
    """This field indicates where in the datagram this fragment belongs.
    
    See RFC 791 for more.
    """
    bits = 13
    auto = True
    def _generate_value(self):
        # TODO: implementation of fragmentation
        # otherwise we can simple return 0 ;-)
        return 0

class HTTL(IntField):
    """This field indicates the maximum time the datagram is allowed to
    remain in the internet system.
    
    See RFC 791 for more.
    """
    bits = 8
    auto = True
    def _generate_value(self):
        # TODO: checking platform to get correct value of TTL
        # unfortunately, there isn't any official document which described
        # list of returns from sys.platform
        # also, there is some changes in Python 2.6 about sys.platform
        return const.TTL_LINUX

    def ttl(self, name):
        """To set correct value of TTL for following platforms:
        AIX, DEC, FREEBSD, HPUX, IRIX, LINUX, MACOS, OS2, SOLARIS,
        SUNOS, ULTRIX, WINDOWS.

        name argument can be pass as shown above or as TTL_NAME
        """

        if not name.startswith("TTL_"):
            name = "TTL_" + name
        self._value = getattr(const, name)

class HProtocol(SpecialIntField):
    """This field indicates the next level protocol used in the data portion
    of the internet datagram.
    
    See RFC 791 for more.
    """
    bits = 8
    auto = True
    def _generate_value(self):
        return self._tmp_value

class HHeaderChecksum(IntField):
    """A checksum on the header only.
    
    See RFC 791 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        return 0        # HeaderChecksum field should be initialized by 0

class HPadding(PaddingField, SpecialIntField):
    """The internet header padding is used to ensure that the internet header
    ends on a 32 bit boundary.
    
    See RFC 791 for more.
    """
    bits = 0
    auto = True

    def _generate_value(self):
        return (32 - (self._tmp_value % 32)) % 32

# main IP class

class IP(Protocol):
    """This is Internet Protocol.
    The main protocol in third layer of OSI model.
    """
    layer = 3      # layer of OSI
    protocol_id = const.ETHERTYPE_IP

    _ordered_fields = ('_version', '_ihl', 'type_of_service', '_total_length',
                    '_identification', 'flags', '_fragment_offset',
                    'time_to_live', '_protocol', '_header_checksum',
                    'source_address', 'destination_address', 'options',
                    '_padding',)

    def __init__(self, **kw):
        tos = ('precedence0','precedence1', 'precedence2', 'delay',
                'throughput', 'relibility', 'reserved0', 'reserved1')
        tos_predefined = dict.fromkeys(tos, 0)

        flags = ('reserved', 'df', 'mf')
        flags_predefined = dict.fromkeys(flags, 0)

        # TODO:
        #   - support for fragmentation
        #       defaulty we don't you fragmentation but we should support it
        #       if user choose this option
        #   - checking platform for TTL value
        #       to be more reliable we should generate default value depends on
        #       user platform. does anyone know every values of sys.platform? :)
        fields_list = [ HVersion("Version", 4), HIHL("IHL"),
                        Flags("TOS", tos, **tos_predefined),
                        HTotalLength("Total Length"),
                        HIdentification("Identification", 0),
                        Flags("Flags", flags, **flags_predefined),
                        HFragmentOffset("Fragment Offset", 0),
                        HTTL("TTL", const.TTL_LINUX), HProtocol("Protocol"),
                        HHeaderChecksum("Header Checksum", 0),
                        IPv4AddrField("Source Address", "127.0.0.1"),
                        IPv4AddrField("Destination Address", "127.0.0.1"),
                        Flags("Options", ()), HPadding("Padding") ]

        # we call super.__init__ after prepared necessary data
        super(IP, self).__init__(fields, **kw)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._get_field('type_of_service').set_doc("The Type of Service \
provides an indication of the abstract parameters of the quality of service \
desired. See RFC 791 for more.")
        self._get_field('flags').set_doc("Various Control Flags. See RFC 791 \
for more.")
        self._get_field('source_address').set_doc("The source address. \
See RFC 791 for more.")
        self._get_field('destination_address').set_doc("The destination \
address. See RFC 791 for more.")
        self._get_field('options').set_doc("The options may appear or not in \
datagrams. See RFC 791 for more.")

    def _is_valid(self, name):
        """Check if attribute is allowed."""
        return self._fields.has_key(name)

    def _raw(self, protocol_container, protocol_bits):
        bit = 0
        raw_value = 0

        # Padding
        self._get_field('_padding')._tmp_value = \
                                                self._get_field('options').bits

        # IHL
        # we store sum of option and padding bits in the _temp_value
        # we can't overwrite _value because user might set his own value there
        # later, generate_value() will return correct value
        self._get_field('_ihl')._tmp_value = \
            self._get_field('options').bits + self._get_field('_padding').bits

        # Total Length
        # we sum length of upper layers and IP layer
        self._get_field('_total_length')._tmp_value = \
            self._get_field('_ihl')._generate_value()*32 + protocol_bits

        # Protocol
        # field indicates the next level protocol used in the data
        # portion of the internet datagram.
        it = iter(protocol_container)
        for proto in it:
            if proto is self:
                break
        try:
            proto = it.next()
            proto_id = proto.protocol_id
        except StopIteration:
            proto_id = 0 # FIXME: what's the default value for non-upper layer?
        finally:
            self._get_field('_protocol')._tmp_value = proto_id

        # so we make a big number with bits of every fields of the protocol
        for field in reversed(self._ordered_fields):
            x = self._get_field(field).fillout()
            raw_value |= x << bit
            bit += self._get_field(field).bits
        # Header Checksum
        # a checksum on the header only.
        cksum_offset = bit - self.get_offset('_header_checksum') - \
                            self._get_field('_header_checksum').bits
        # check if user doesn't provide own values of bits
        if (raw_value & (0xff << cksum_offset)) >> cksum_offset == 0:
            # calculate and add checksum to the raw_value
            cksum = net.in_cksum(raw_value)
            raw_value |= cksum << cksum_offset

        return raw_value, bit

protocols = [ IP, ]
