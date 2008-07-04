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
        #try:
        self._sock = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
        utils.leave_priviliges()    # dropping root-priviliges
        #except error, msg:
        #    sys.stderr.write('Error while opening new socket:\n')
        #    sys.stderr.write(str(msg) + '\n')
        #    sys.stderr.write('Leaving...')
        #    sys.exit(1)

    def send(self, *packets):
        '''Sending your packets'''

        for packet in packets:
            self._sock.send(packet.get_raw())
