#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
#
# Author: Gaurav Ranjan < g.ranjan143@gmail.com>
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
Usefull classes for 4th layer's protocols.

TCP/UDP use special pseudo header to calculate checksum. These classes
are provided.
"""

from umit.umpa.protocols._protocols import Protocol
from umit.umpa.protocols.IPV6 import IPV6
from umit.umpa.protocols._fields import IntField, IPv4AddrField, IPv6AddrField

class Layer4ChecksumField(IntField):
    """
    A checksum for the common classes of 4th layer of OSI model.

    Especially UDP/TCP use it. The checksum is calculated from the Pseudo
    Header, the main header and the payload.    
    """

    bits = 16
    auto = True

    def _generate_value(self):
        """
        """

        return 0

class PseudoHeader6(Protocol):
    """
    This is Pseudo Header.
    
    This class is useful for some protocols like TCP or UDP.
    It's used to calculate checksum of those protocols.
    It's prefixed to the protocol header before calculating.
    """

    _ordered_fields = ('src', 'dst', 'up_layer_length',
                    'zero', 'protocol_id')

    def __init__(self, protocol_id, total_length):
        """
        Create a new PseudoHeader()

        @type protocol_id: C{int}
        @param protocol_id: id of the protocol which use PseudoHeader.

        @type total_length: C{int}
        @param total_length: length of the real header and payload.
        """
		
        fields_list = [ IPv6AddrField("Source Address"),
                        IPv6AddrField("Destination Address"),
                        IntField("Upper layer length", total_length, bits=32),
                        IntField("zero", 0, bits=24),
                        IntField("Next Header ", protocol_id , bits=8) ]
        super(PseudoHeader6, self).__init__(fields_list)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        Parse lower protocol (usually IP) to get source/destination address.

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

        # assign localhost first becuase if there is none IP instance
        self.src = "0000:0000:0000:0000:0000:0000:0000:0001"
        self.dst = "0:0:0:0:0:0:0:1"
        # grabbing informations from the IP's header
        it = iter(protocol_container)
        for proto in it:
            if isinstance(proto, IPV6):
                self.src = proto.src
                self.dst = proto.dst
                break

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields after calling fillout() for them.

        Nothing to do for PseudoHeader class here. Return required vars.

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
