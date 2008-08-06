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
from umpa.protocols._layer4 import *
from umpa.utils import net

class HSequenceNumber(IntField):
    """The sequence number of the first data octet in this segment (except
    when SYN is present).

    See RFC 793 for more.
    """
    bits = 32
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class HAcknowledgmentNumber(IntField):
    """If the ACK control bit is set this field contains the value of the
    next sequence number the sender of the segment is expecting to receive.

    See RFC 793 for more.
    """
    bits = 32
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 1

class HDataOffset(SpecialIntField):
    """The number of 32 bit words in the TCP Header. This indicates where
    the data begins.

    See RFC 793 for more.
    """
    bits = 4
    auto = True
    def _generate_value(self):
        # returns in 32-bits units
        return 5 + self._tmp_value / 32 # 5 is a minimum value

class HReserved(IntField):
    """Reserved for future use.

    See RFC 793 for more.
    """
    bits = 6
    auto = True
    def _generate_value(self):
        return 0

class HWindow(IntField):
    """The number of data octets beginning with the one indicated in the
    acknowledgment field which the sender of this segment is willing to accept.

    See RFC 793 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 512

class HUrgentPointer(IntField):
    """This field communicates the current value of the urgent pointer as a
    positive offset from the sequence number in this segment.

    See RFC 793 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class TCP(Protocol):
    """This is Transmission Control Protocol.
    It the most common protocol in the Internet on fourth layer
    of the OSI model.
    """
    layer = 4       # layer of the OSI
    protocol_id = const.PROTOCOL_TCP

    _ordered_fields = ('source_port', 'destination_port', '_sequence_number',
                    '_acknowledgment_number', '_data_offset', '_reserved',
                    'control_bits', '_window', '_checksum', '_urgent_pointer',
                    'options', '_padding',)

    def __init__(self, **kw):
        control_bits = ('urg', 'ack', 'psh', 'rst', 'syn', 'fin')
        control_bits_predefined = dict.fromkeys(control_bits, 0)

        fields_list = [ PortField("Source Port", 0),
                        PortField("Destination Port", 0),
                        HSequenceNumber("Sequence Number"),
                        HAcknowledgmentNumber("Acknowledgment Number"),
                        HDataOffset("DataOffset"), HReserved("Reserved", 0),
                        Flags("Control Bits", control_bits,
                        **control_bits_predefined),
                        HWindow("Window"), Layer4ChecksumField("Checksum"),
                        HUrgentPointer("Urgent Pointer"), Flags("Options", ()),
                        PaddingField("Padding") ]

        # we call super.__init__ after prepared necessary data
        super(TCP, self).__init__(fields_list, **kw)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._get_field('source_port').set_doc("The source port number. \
See RFC 793 for more.")
        self._get_field('destination_port').set_doc("The destination port \
number. See RFC 793 for more.")
        self._get_field('control_bits').set_doc("URG, ACK, PSH, RST, SYN, FIN \
flags. See RFC 793 for more.")
        self._get_field('options').set_doc("Options may occupy space at the \
end of the TCP header and are a multiple of 8 bits in length. See RFC 793 \
for more.")
        self._get_field('_padding').set_doc("The TCP header padding is used \
to ensure that the TCP header ends and data begins on a 32 bit boundary. \
See RFC 793 for more.")

    def _raw(self, protocol_container, protocol_bits):
        bit = 0
        raw_value = 0

        # Padding
        self._get_field('_padding')._tmp_value = \
                                                self._get_field('options').bits

        # Data Offset
        self._get_field('_data_offset')._tmp_value = \
            self._get_field('options').bits + self._get_field('_padding').bits

        # so we make a big number with bits of every fields of the protocol
        for field in reversed(self._ordered_fields):
            x = self._get_field(field).fillout()
            raw_value |= x << bit
            bit += self._get_field(field).bits

        cksum_offset = bit - self.get_offset('_checksum') - self._get_field('_checksum').bits
        if (raw_value & (0xff << cksum_offset)) >> cksum_offset == 0:
            cksum = 0
            offset = 0
            # TODO: payload is off. it should works but it's odd, we generate
            # bits by calling get_raw for payload. completely but.
            # also because of some new suggestions about look after of payload
            # very very soon, should be reorgnized payload issue
            # and this issue also
            #
            # Payload
            #it = iter(protocol_container)
            #for proto in it:
            #    if proto is self:
            #        break
            #try:
            #    proto = it.next()
            #    payload = proto._get_raw(protocol_container, protocol_bits)
            #except StopIteration:
            #    payload = 0

            #cksum = payload
            #offset = protocol_bits

            # TCP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # TCP header length...converted to bits unit
            total_length = self._get_field('_data_offset').fillout()*32
            # add payload
            total_length += protocol_bits
            # conversion to bytes unit
            total_length /= 8

            # create pseudo header object
            pheader = PseudoHeader(self.protocol_id, total_length)
            # generate raw value of it
            pheader_bits = pheader._get_raw(protocol_container,
                                                            protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_bits << offset

            # finally, calcute and apply checksum
            raw_cksum = net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_offset

        return raw_value, bit

protocols = [ TCP, ]
