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

"""
Socket connection management.

It contains Socket class which should be used instead of
socket.socket() directly from the standard library.

But it's correctly to use socket module directly if needed.
"""

import sys
import socket

from umpa.utils.exceptions import UMPANotPermittedException

class Socket(object):
    """
    This class handles with sockets.

    To send built packets your need to create a socket.
    You can use socket module from Python Standard Library directly
    but it's recommended to use this class instead.

    That is because there are some other features,
    and for some security issues.
    """

    def __init__(self):
        """
        Create a new Socket().
        """

        # to create socket object we need root priviligies.
        # if non-root EUID, then exception is raised
        # use umpa.utils.security.super_priviliges() to avoid exception
        # when a new Socket object is created
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                                            socket.IPPROTO_RAW)
        except socket.error, msg:
            raise UMPANotPermittedException(msg)

        # to build own headers of IP
        self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    def send(self, *packets):
        """
        Send packets in to the network.

        @type packets: C{Packet}
        @param packets: packets which were built by umpa.Packet objects.
        """

        sent_bits = []
        for packet in packets:
            # XXX: it connects to a remote socket, so destination address has
            # to be known. the better solution would be to use Ethernet 
            # protocol (the lowest software layer from OSI).
            # it will be implemented when Ethernet protocol will be implemented
            # so now we have to parse the packet for destination address
            dst_addr = self._get_address(packet)
            sent_bits.append(self._sock.sendto(packet._get_raw(),
                                                                (dst_addr,0)))
        return sent_bits

    def _get_address(self, packet):
        """
        Pick out the destination address from 3rd layer.

        Because of the Ethernet issue (check the comments in send() method for
        more), we have to parse packets for destination addresses.

        @return: destination address from 3rd layer of OSI model.
        """
        for p in packet.protos:
            if p.layer == 3:    # XXX: if we included more than one protocol
                break           #      of layer 3 we got IP from the first one
        return p.destination_address
