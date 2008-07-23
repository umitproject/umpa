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

from _ import *
from umpa.utils.my_exceptions import UMPAAttributeException

class HIHL(IntField):
    bits = 4
    def generate_value(self):
        pass
        # FIXME: how to get length of every fields in this scope?

class HTotalLength(Field):
    bits = 16
    def fillout(self):
        pass

class HIdentification(Field):
    bits = 16
    def fillout(self):
        pass

class HFragmentOffset(Field):
    bits = 13
    def fillout(self):
        pass

class HProtocol(Field):
    bits = 8
    def fillout(self):
        pass

class HHeaderChecksum(Field):
    bits = 16
    def fillout(self):
        pass

class HPadding(Field):
    bits = 0
    def fillout(self):
        pass

# main IP class

class IP(Protocol):
    """This is Internet Protocol.
    The main protocol in third layer of OSI model.
    """
    layer = 3      # layer of OSI

    _ordered_fields = ('_version', '_ihl', 'type_of_service', '_total_length',
                    '_identification', 'flags', '_fragment_offset',
                    'time_to_live', '_protocol', '_header_checksum',
                    'source_address', 'destination_address', 'options',
                    '_padding',)

    def __init__(self, **kw):
        tos = ('precedence0','precedence1', 'precedence2', 'delay',
                'throughput', 'relibility', 'reserved0', 'reserverd1')
        flags = ('reserved', 'df', 'mf')

        fields_list = [ IntField("Version", 4, 4), HIHL("IHL"),
                        Flags("TOS",tos), HTotalLength("Total Length"),
                        HIdentification("Identification"),
                        Flags("Flags", flags, reserved=0),
                        HFragmentOffset("Fragment Offeset"),
                        Field("TTL", 255, 8), HProtocol("Protocol"),
                        HHeaderChecksum("Header Checksum"),
                        Field("Source Address", bits=16),
                        Field("Destination Address", bits=16),
                        Flags("Options", ()), HPadding("Padding") ]

        # we pack objects of header's fields to the dict
        fields = dict(zip(self._ordered_fields, fields_list))
        super(IP, self).__init__(fields, **kw)

        # setting up passed fields
        for field in kw:
            self.__setattr__(field, kw[field])


        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._fields['_version'].set_doc("The Version field indicates the \
format of the internet header. See RFC 791 for more.")
        self._fields['_ihl'].set_doc("Internet Header Length is the length \
of the internet header in 32 bit words, and thus points to the beginning of \
the data. See RFC 791 for more.")
        self._fields['type_of_service'].set_doc("The Type of Service provides \
an indication of the abstract parameters of the quality of service desired. \
See RFC 791 for more.")
        self._fields['_total_length'].set_doc("Total Length is the length of \
the datagram, measured in octets, including internet header and data. \
See RFC 791 for more.")
        self._fields['_identification'].set_doc("An identifying value \
assigned by the sender to aid in assembling the fragments of a datagram. \
See RFC 791 for more.")
        self._fields['flags'].set_doc("Various Control Flags. See RFC 791 \
for more.")
        self._fields['_fragment_offset'].set_doc("This field indicates where \
in the datagram this fragment belongs. See RFC 791 for more.")
        self._fields['time_to_live'].set_doc("This field indicates the \
maximum time the datagram is allowed to remain in the internet system. \
See RFC 791 for more.")
        self._fields['_protocol'].set_doc("This field indicates the next \
level protocol used in the data portion of the internet datagram. See RFC 791 \
for more.")
        self._fields['_header_checksum'].set_doc("A checksum on the header \
only. See RFC 791 for more.")
        self._fields['source_address'].set_doc("The source address. \
See RFC 791 for more.")
        self._fields['destination_address'].set_doc("The destination address. \
See RFC 791 for more.")
        self._fields['options'].set_doc("The options may appear or not in \
datagrams. See RFC 791 for more.")
        self._fields['_padding'].set_doc("The internet header padding is used \
to ensure that the internet header ends on a 32 bit boundary. See RFC 791 for \
more.")

    def _is_valid(self, name):
        """Check if attribute is allowed."""
        return self._fields.has_key(name)

protocols = [ IP, ]
