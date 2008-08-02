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

import sys
from socket import *

import umpa.utils.security
from umpa.utils import UMPAException

class Socket(object):
    """To send built packets your need to create a socket.
    You can use socket module from Python Standard Library directly
    but it's recommended to use this class instead.
    That is because there is some other features, and for some security issues.
    """
    def __init__(self):
        """This is a default constructor for Socket's class.
        Just use it in any doubts.
        """
        # XXX: if non-root EUID, then exception is raised
        # TODO: before raising UMPAException, we can try
        # to switch EUID into root and recall socket()
        try:
            self._sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
            # dropping root-priviliges
            umpa.utils.security.drop_priviliges()
        except error, msg:
            raise UMPAException(msg)
        # to build own headers of IP
        self._sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

    def send(self, *packets):
        """Sending your packets"""

        for packet in packets:
            # XXX: this connects to a remote socket, so destination address has to be known.
            # the better solution would be to use ARP (the lowest software layer from OSI).
            # it will be implemented when ARP protocol will be implemented ;)
            # so now we have to parse the packet for destination address
            dst_addr = self._get_address(packet)
            self._sock.sendto(packet.get_raw(), (dst_addr,0) )

    def _get_address(self, packet):
        """Because of Ethernet issue (described in send() method,
        we have to parse packets for destination addresses.
        """
        for p in packet.protos:
            if p.layer == 3:    # XXX: if we included more than one protocol
                break           #      of layer 3 we got IP from the first one
        return p.destination_address
