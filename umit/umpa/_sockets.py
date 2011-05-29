#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2010 Adriano Monteiro Marques.
#
# Authors: Bartosz SKOWRON <getxsick at gmail dot com>
#          Kosma Moczek <kosma at kosma dot pl>
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
Raw sockets support.

Contains Socket classes which can be used to send raw packets in
a platform-independent manner. The standard Python socket module can be used
instead if advanced functionalities are needed.
"""

import socket
import struct
import sys
import os
from errno import EBUSY

from umit.umpa.utils.exceptions import UMPAException, UMPANotPermittedException

# constants from various header files not available under Python
ETH_P_ALL = 3                     # from linux/if_ether.h
BIOCSETIF = 2149597804            # from net/bpf.h

# Detect socket programming model. This greatly simplifies socket code.

#
#need to add AF_INET6 for ipv6 or we can use AF_UNSPEC for l3model so thatit accept any address 
#
if sys.platform == 'linux2':
    _l2model = 'AF_PACKET'
    _l3model = 'AF_UNSPEC'
    _l3quirk = None
elif sys.platform.startswith('freebsd') or \
     sys.platform.startswith('netbsd') or \
     sys.platform.startswith('darwin'):
    _l2model = 'bpf'
    _l3model = 'AF_UNSPEC'
    _l3quirk = 'ntohs'
elif sys.platform.startswith('openbsd'):
    _l2model = 'bpf'
    _l3model = 'AF_UNSPEC'
    _l3quirk = None
elif os.name == 'nt':
    _l2model = 'NDIS'
    _l3model = 'AF_UNSPEC'
    _l3quirk = 'windows'
else:
    _l2model = None
    _l3model = None
    _l3quirk = None

# load additional modules conditionally depending on programming models
if _l2model == 'bpf':
    from fcntl import ioctl

def send(*packets, **kwargs):
    """
    Send arbitrary packets.

    The function creates sockets of proper level as needed. The 'iface'
    named argument must be supplied for L2 (link-layer) sockets.

    @type packets: C{Packet}
    @param packets: list of umit.umpa.Packet objects to send.

    @returns: List of return values (byte counts) from the send() function.
    """

    sent_bytes = []
    for packet in packets:
        # create appropriate socket based on packet's lowermost layer
        if packet.protos[0].layer == 2:
            sock = SocketL2(iface=kwargs.get('iface'))
        else:
            sock = SocketL3()
        sent_bytes.extend(sock.send(packet))
    return sent_bytes

class _Socket(object):
    """
    Raw socket superclass.

    This is an abstract class.
    """

    def __init__(self, **kwargs):
        raise NotImplementedError("this is an abstract class")

class SocketL2(_Socket):
    """
    Level 2 (link-layer) socket class.

    Supported platforms: Linux (AF_PACKET), BSD (bpf).
    """

    def __init__(self, iface=None):
        """
        Create a new SocketL2 instance.

        Requires root/administrator rights and/or CAP_NET_RAW capability.

        @type iface: C{str}
        @param iface: Interface to use for sending the packets.
        """
        if iface is None:
            # TODO: port interface detection from the link-layer branch
            raise NotImplementedError("You need to specify iface")

        if _l2model == 'AF_PACKET':
            try:
                self._sock = socket.socket(socket.AF_PACKET,
                        socket.SOCK_RAW,
                        ETH_P_ALL)
            except socket.error, msg:
                raise UMPANotPermittedException(msg)

            self._sock.bind((iface, ETH_P_ALL))
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**20)
        elif _l2model == 'bpf':
            # Loop over /dev/bpf* devices, looking for a free one.
            self._sock = None
            suffix = 0
            while self._sock is None:
                try:
                    self._sock = open('/dev/bpf'+str(suffix), 'wb')
                except IOError, error:
                    if error.errno == EBUSY:
                        suffix = suffix + 1
                    else:
                        raise UMPAException(str(error))

            ioctl(self._sock, BIOCSETIF, iface)
        else:
            raise NotImplementedError("L2 sockets unsupported on your platform")

    def send(self, *packets):
        """
        Send packets through the socket.

        @type packets: C{Packet}
        @param packets: List of umit.umpa.Packet objects to send.

        @returns: List of return values (byte counts) from the send() function.
        """

        sent_bytes = []
        for packet in packets:
            if _l2model == 'AF_PACKET':
                sent_bytes.append(self._sock.send(packet.get_raw()))
            elif _l2model == 'bpf':
                sent_bytes.append(self._sock.write(packet.get_raw()))
            else:
                raise NotImplementedError("L2 send unsupported on your platform")
        return sent_bytes

class SocketL3(_Socket):
    """
    Level 3 (network layer) socket class.

    Supported platforms: Linux, BSD, Windows (AF_INET).

    Note: If you plan to use raw sockets under Windows XP SP2 or later, be aware
    of the restrictions imposed by the Windows’ networking stack. They generally
    boil down to two things:

    1. TCP data cannot be sent over raw sockets.
    2. The IP source address for any outgoing UDP datagram must exist on
       a network interface.

    The detailed description of those restrictions can be found at the following URL:
    http://msdn.microsoft.com/en-us/library/ms740548%28VS.85%29.aspx. If you find
    them to be too limiting, consider using Layer 2 sockets (SocketL2 class) instead.
    """

    def __init__(self):
        """
        Create a new SocketL3 instance.

        Requires root/administrator rights and/or CAP_NET_RAW capability.
        """
		#
		#here create socket for AF_UNSPEC and and while sending the packet in send 
		#use any ipaddress (IPv4 or IPv6)
		#
		#
        if _l3model == 'AF_UNSPEC':
            try:
                self._sock = socket.socket(socket.AF_UNSPEC,
                                           socket.SOCK_RAW,
                                           socket.IPPROTO_RAW)
            except socket.error, msg:
                raise UMPANotPermittedException(msg)

            # tell the kernel we are including our own IP header
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        else:
            raise NotImplementedError('L3 sockets unsupported on your platform')

    def send(self, *packets):
        """
        Send packets through the socket.

        @type packets: C{Packet}
        @param packets: List of umit.umpa.Packet objects to send.

        @returns: List of return values (byte counts) from the send() function.
        """

        sent_bytes = []
        for packet in packets:
            if _l3model == 'AF_UNSPEC':
                # get destination address and convert it to IPv4 notation
                # TODO: move this to utils.net
                dst_addr = packet._get_destination(layer=3)
                #
                #Here check the destination address thet whether it is ipv4 or ipv6
                #
                #
                if type(dst_addr) is tuple:
                	if len(dst_addr) == 6:
                    	dst_addr = ".".join(str(y) for y in dst_addr)
                    else:
                    	dst_addr = ":".join(str(y) for y in dst_addr)

                raw = packet.get_raw()

                if _l3quirk == 'ntohs':
                    raw = _ntohs_quirk(raw)

                sent_bytes.append(self._sock.sendto(raw, (dst_addr, 0)))
            else:
                raise NotImplementedError("L3 send unsupported on your platform")
        return sent_bytes

def _ntohs_quirk(raw):
    """
    FreeBSD raw socket endianness quirk support.

    Some BSD flavors, notably FreeBSD, have a weirdness in their raw IP sockets
    in that the 'total length' and 'fragment offset' fields must be supplied in
    host byte order. See ip(4) manpage on affected systems.

    This function corrects the endianness of a packet, making it suitable to be
    sent on such systems.

    @type raw: C{str}
    @param raw: Raw IP header

    @returns: Raw IP header data with 'total length' and 'fragment offset' fields
              converted to host byte order.
    """

    vhds, tl, id, fo = struct.unpack("!HHHH", raw[0:8])
    tl = socket.ntohs(tl)
    fo = socket.ntohs(fo)
    raw = struct.pack("!HHHH", vhds, tl, id, fo) + raw[8:]

    return raw

# XXX API compatibility hack for Milestone 0.3 release
Socket = SocketL3
