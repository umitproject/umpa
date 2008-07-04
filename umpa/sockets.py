#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys
from socket import *

import utils


class Socket:
    '''To send built packets your need to create a socket.
    You can use socket module from Python Standard Library directly
    but it's recommended to use this class instead.
    That is because there is some other features, and for some security issues.
    '''
    def __init__(self):
        '''This is a default constructor for Socket's class.
        Just use it in any doubts.
        '''
        # XXX: if non-root EUID, then Python will exit the application
        # and report the error
        # TODO: try/except section + trying to switch EUID into root and recall socket()
        self._sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
        # dropping root-priviliges
        utils.drop_priviliges()    
        # to build own headers of IP
        self._sock.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

    def send(self, *packets):
        '''Sending your packets'''

        for packet in packets:
            # XXX: this connects to a remote socket, so destination address has to be known.
            # the better solution would be to use ARP (the lowest software layer from OSI).
            # it will be implemented when ARP protocol will be implemented ;)
            # so now we have to parse the packet for destination address
            dst_addr = self._get_address(packet)
            self._sock.sendto(packet.get_raw(), (dst_addr,0) )

    def _get_address(self, packet):
        '''Because of ARP issue (described in send() method,
        we have to parse packets for destination addresses.
        '''
        print "Not implemented yet."
        return False
