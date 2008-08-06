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
from umpa.utils import bits

class HLength(SpecialIntField):
    """Length  is the length  in octets  of this user datagram  including  this
    header  and the data.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # returns in byte units
        return 8 + self._tmp_value/8    # minimum is 8

class UDP(Protocol):
    """This is User Datagram Protocol.
    
    This protocol  provides  a procedure  for application  programs  to send
    messages  to other programs  with a minimum  of protocol mechanism.  The
    protocol  is transaction oriented, and delivery and duplicate protection
    are not guaranteed.
    """
    layer = 4
    protocol_id = const.PROTOCOL_UDP

    _ordered_fields = ('source_port', 'destination_port', '_length',
                                                            '_checksum')

    def __init__(self, **kw):
        fields_list = [ PortField("Source Port", 0),
                        PortField("Destination Port", 0),
                        HLength("Length"),
                        Layer4ChecksumField("Checksum"), ]

        # we call super.__init__ after prepared necessary data
        super(UDP, self).__init__(fields_list, **kw)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._get_field('source_port').set_doc("The source port number. \
See RFC 768 for more.")
        self._get_field('destination_port').set_doc("The destination port \
number. See RFC 768 for more.")
        self._get_field('_checksum').set_doc("Checksum of Pseudo Header, UDP \
header and data. See RFC 768 for more.")

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        # Length
        self._get_field('_checksum')._tmp_value = protocol_bits

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        cksum_rev_offset = 0
        # checking if user not defined his own value of checksum
        if bits.get_bits(raw_value, self._get_field('_checksum').bits,
                                    cksum_rev_offset, rev_offset=True) == 0:
            # Payload
            if self.payload:
                cksum = self.payload.__raw_value
            else:
                cksum = 0
            offset = protocol_bits

            # UDP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # create pseudo header object
            pheader = PseudoHeader(self.protocol_id,
                                        self._get_field('_length').fillout())
            # generate raw value of it
            pheader_bits = pheader._get_raw(protocol_container,
                                                        protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_bits << offset

            # finally, calcute and apply checksum
            raw_cksum = net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_rev_offset

        return raw_value, bit

protocols = [ UDP, ]
