#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
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

import threading
import time

import umit.umpa

class SendPacket(threading.Thread):
    def __init__(self, packet, amount=1):
        super(SendPacket, self).__init__()
        self._packet = packet
        self._amount = amount
    def run(self):
        s = umit.umpa.Socket()
        for i in xrange(self._amount):
            time.sleep(2)
            s.send(self._packet)

class SendPacketL2(threading.Thread):
    def __init__(self, packet, amount=1, iface=None):
        super(SendPacketL2, self).__init__()
        self._packet = packet
        self._amount = amount
        self._iface  = iface
    def run(self):
        s = umit.umpa.SocketL2(iface=self._iface)
        for i in xrange(self._amount):
            time.sleep(2)
            s.send(self._packet)
