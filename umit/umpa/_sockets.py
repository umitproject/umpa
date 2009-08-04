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
Socket connection management.

It contains Socket class which should be used instead of
socket.socket() directly from the standard library.

But it's correctly to use socket module directly if needed.
"""

import socket

from umit.umpa.utils.exceptions import UMPAException, UMPANotPermittedException

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
        # use umit.umpa.utils.security.super_priviliges() to avoid exception
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
        @param packets: packets which were built by umit.umpa.Packet objects.
        """

        sent_bits = []
        for packet in packets:
            sent_bits.append(self._sock.sendto(packet.get_raw(),
                                                            ('127.0.0.1', 0)))
        return sent_bits
