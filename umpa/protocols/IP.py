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
IP (Internet Protocol) protocol implementation.
"""

import sys

from umpa.protocols import _consts
from umpa.protocols import _fields
from umpa.protocols import _protocols
import umpa.utils.net as _net
import umpa.utils.bits as _bits

__all__ = [ "IP", ]

class _HVersion(_fields.EnumField):
    """
    The Version field indicates the format of the internet header.
    
    See RFC 791 for more.
    """
    
    bits = 4
    auto = True
    enumerable = {
        "Reserved (0)"      : _consts.IPVERSION_RESERVED0,
        "Internet Protocol" : _consts.IPVERSION_4,
        "ST Datagram Mode"  : _consts.IPVERSION_ST_DATAGRAM_MODE,
        "Reserved (15)"     : _consts.IPVERSION_RESERVED15
    }

    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return _consts.IPVERSION_4

class _HIHL(_fields.SpecialIntField):
    """
    Internet Header Length is the length of the internet header in 32 bit
    words, and thus points to the beginning of the data.
    
    See RFC 791 for more.
    """

    bits = 4
    auto = True

    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return 5 + self._tmp_value / 32 # 5 is a minimum value (see RFC 791)

class _HTotalLength(_fields.SpecialIntField):
    """
    Total Length is the length of the datagram, measured in octets,
    including internet header and data.

    See RFC 791 for more.
    """

    bits = 16
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return self._tmp_value / _consts.BYTE

class _HIdentification(_fields.IntField):
    """
    An identifying value assigned by the sender to aid in assembling the
    fragments of a datagram.

    See RFC 791 for more.
    """
    
    bits = 16
    auto = True

    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implementation of fragmentation
        # otherwise we can simple return 0 ;-)
        return 0

class _HFragmentOffset(_fields.IntField):
    """
    This field indicates where in the datagram this fragment belongs.
    
    See RFC 791 for more.
    """
    
    bits = 13
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implementation of fragmentation
        # otherwise we can simple return 0 ;-)
        return 0

class _HTTL(_fields.EnumField):
    """
    This field indicates the maximum time the datagram is allowed to
    remain in the internet system.
    
    See RFC 791 for more.
    """
    
    bits = 8
    auto = True
    enumerable = {
        "aix"       : _consts.TTL_AIX,
        "dec"       : _consts.TTL_DEC,
        "freebsd"   : _consts.TTL_FREEBSD,
        "irix"      : _consts.TTL_IRIX,
        "linux"     : _consts.TTL_LINUX,
        "macos"     : _consts.TTL_MACOS,
        "os2"       : _consts.TTL_OS2,
        "solaris"   : _consts.TTL_SOLARIS,
        "sunos"     : _consts.TTL_SUNOS,
        "ultrix"    : _consts.TTL_ULTRIX,
        "windows"   : _consts.TTL_WINDOWS,
    }
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        if sys.platform.find('linux') != -1:
            result = 'linux'
        elif sys.platform.find('darwin') != -1:
            result = 'macos'
        elif sys.platform.find('win') != -1:
            result = 'windows'
        elif sys.platform.find('freebsd') != -1:
            result = 'freebsd'
        elif sys.platform.find('os2') != -1:
            result = 'os2'
        elif sys.platform.find('sunos') != -1:
            result = 'sunos'
        elif sys.platform.find('aix') != -1:
            result = 'aix'
        elif sys.platform.find('irix') != -1:
            result = 'irix'
        elif sys.platform.find('solaris') != -1:
            result = 'solaris'
        elif sys.platform.find('ultrix') != -1:
            result = 'ultrix'
        elif sys.platform.find('dec') != -1:
            result = 'dec'
        else:
            result = 'linux'

        return self.enumerable[result]

class _HProtocol(_fields.SpecialIntField, _fields.EnumField):
    """
    This field indicates the next level protocol used in the data portion
    of the internet datagram.
    
    See RFC 791 for more.
    """

    bits = 8
    auto = True
    enumerable = {
        "Reserved (0)"                      : _consts.PROTOCOL_RESERVED0,
        "ICMP"                              : _consts.PROTOCOL_ICMP,
        "Gateway-to-Gateway"                :
                                        _consts.PROTOCOL_GATEWAY_TO_GATEWAY,
        "CMCC Gateway Monitoring Message"   : _consts.PROTOCOL_CMCC,
        "ST"                                : _consts.PROTOCOL_ST,
        "TCP"                               : _consts.PROTOCOL_TCP,
        "UCL"                               : _consts.PROTOCOL_UCL,
        "Secure"                            : _consts.PROTOCOL_SECURE,
        "BBN RCC Monitoring"                :
                                        _consts.PROTOCOL_BBN_RCC_MONITORING,
        "NVP"                               : _consts.PROTOCOL_NVP,
        "PUP"                               : _consts.PROTOCOL_PUP,
        "Pluribus"                          : _consts.PROTOCOL_PLURIBUS,
        "Telenet"                           : _consts.PROTOCOL_TELENET,
        "XNET"                              : _consts.PROTOCOL_XNET,
        "Chaos"                             : _consts.PROTOCOL_CHAOS,
        "UDP"                               : _consts.PROTOCOL_UDP,
        "Multiplexing"                      : _consts.PROTOCOL_MULTIPLEXING,
        "DCN"                               : _consts.PROTOCOL_DCN,
        "TAC Monitoring"                    : _consts.PROTOCOL_TAC_MONITORING,
        "any local network"                 : _consts.PROTOCOL_ANY,
        "SATNET and Backroom EXPAK"         :
                                        _consts.PROTOCOL_SATNET_BACKROOM_EXPAK,
        "MIT Subnet Support"                :
                                        _consts.PROTOCOL_MIT_SUBNET_SUPPORT,
        "SATNET Monitoring"                 :
                                        _consts.PROTOCOL_SATNET_MONITORING,
        "Internet Packet Core Utility"      :
                                _consts.PROTOCOL_INTERNET_PACKET_CORE_UTILITY,
        "Backroom SATNET Monitoring"        :
                                _consts.PROTOCOL_BACKROOM_SATNET_MONITORING,
        "WIDEBAND Monitoring"               :
                                        _consts.PROTOCOL_WIDEBAND_MONITORING,
        "WIDEBAND EXPAK"                    : _consts.PROTOCOL_WIDEBAND_EXPAK,
        "Reserved (255)"                    : _consts.PROTOCOL_RESERVED255
    }

    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return self._tmp_value

class _HHeaderChecksum(_fields.IntField):
    """
    A checksum of the header only.
    
    See RFC 791 for more.
    """
    
    bits = 16
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return 0        # HeaderChecksum field should be initialized by 0

# main IP class

class IP(_protocols.Protocol):
    """
    Internet Protocol implementation.

    The main protocol in third layer of OSI model.
    """

    layer = 3      # layer of OSI
    protocol_id = _consts.ETHERTYPE_IP
    name = "IP"

    _ordered_fields = ('_version', '_ihl', 'type_of_service', '_total_length',
                    '_identification', 'flags', '_fragment_offset',
                    'time_to_live', '_protocol', '_header_checksum',
                    'source_address', 'destination_address', 'options',
                    '_padding',)

    def __init__(self, **kwargs):
        """
        Create a new IP().
        """

        tos = ('precedence0', 'precedence1', 'precedence2', 'delay',
                'throughput', 'relibility', 'reserved0', 'reserved1')
        tos_predefined = dict.fromkeys(tos, 0)

        flags = ('reserved', 'df', 'mf')
        flags_predefined = dict.fromkeys(flags, 0)

        # TODO:
        #   - support for fragmentation
        #       defaulty we don't use fragmentation but we should support it
        #       if user choose this option
        fields_list = [ _HVersion("Version", 4),
                        _HIHL("IHL"),
                        _fields.Flags("TOS", tos, **tos_predefined),
                        _HTotalLength("Total Length"),
                        _HIdentification("Identification", 0),
                        _fields.Flags("Flags", flags, **flags_predefined),
                        _HFragmentOffset("Fragment Offset", 0),
                        _HTTL("TTL"),
                        _HProtocol("Protocol"),
                        _HHeaderChecksum("_Header Checksum", 0),
                        _fields.IPv4AddrField("Source Address", "127.0.0.1"),
                        _fields.IPv4AddrField("Destination Address",
                                                                "127.0.0.1"),
                        _fields.Flags("Options", ()),
                        _fields.PaddingField("Padding") ]

        # we call super.__init__ after prepared necessary data
        super(IP, self).__init__(fields_list, **kwargs)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self.get_field('type_of_service').set_doc("The Type of Service "
            "provides an indication of the abstract parameters of the quality "
            "of service desired. See RFC 791 for more.")
        self.get_field('flags').set_doc("Various Control Flags. See RFC 791 " 
            "for more.")
        self.get_field('source_address').set_doc("The source address. "
            "See RFC 791 for more.")
        self.get_field('destination_address').set_doc("The destination "
            "address. See RFC 791 for more.")
        self.get_field('options').set_doc("The options may appear or not in "
            "datagrams. See RFC 791 for more.")
        self.get_field('_padding').set_doc("The internet header padding is "
            "used to ensure that the internet header ends on a 32 bit "
            "boundary. See RFC 791 for more.")

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

        # Padding
        self.get_field('_padding')._tmp_value = self.get_field('options').bits

        # IHL
        # we store sum of option and padding bits in the _temp_value
        # we can't overwrite _value because user might set his own value there
        # later, generate_value() will return correct value
        self.get_field('_ihl')._tmp_value = \
            self.get_field('options').bits + self.get_field('_padding').bits

        # Total Length
        # we sum length of upper layers and IP layer
        self.get_field('_total_length')._tmp_value = \
            self.get_field('_ihl').fillout()*32 + protocol_bits

        # Protocol
        # field indicates the next level protocol used in the data
        # portion of the internet datagram.
        if self.payload:
            proto_id = self.payload.protocol_id
        else:
            proto_id = 0 # FIXME: what's the default value for non-upper layer?
        self.get_field('_protocol')._tmp_value = proto_id

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

        # Header Checksum
        # a checksum on the header only.
        cksum_offset = bit - self.get_offset('_header_checksum') - \
                                    self.get_field('_header_checksum').bits
        # check if user doesn't provide own values of bits
        if _bits.get_bits(raw_value,
                        self.get_field('_header_checksum').bits,
                        cksum_offset,
                        rev_offset=True) == 0:
            # calculate and add checksum to the raw_value
            cksum = _net.in_cksum(raw_value)
            raw_value |= cksum << cksum_offset

        return raw_value, bit

protocols = [ IP, ]
