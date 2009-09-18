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

# this example shows how to send broken packets with not saved layers order

import time
import threading

import umit.umpa
from umit.umpa.extensions import models
from umit.umpa.protocols import IP, TCP, Payload

# models it's just to make our life easier

# react mechanism is used to simple resend packet back with small modifications

# prepare packet which we want to react on
# to get possibility of sniffing and sending packets at the same
# we use threads where after a small delay we send a packet
#
# obviously it's not necessary in real usecase
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

packet = umit.umpa.Packet(IP(src="1.2.3.4", dst="127.0.0.1"),
                    TCP(srcport=99), Payload(data="sniff me"))

# run thread and send 2 packets
th = SendPacket(packet, 2)
th.start()

# capture 2 packets and resend them with reverse src/dst ports
models.react(2, filter="host 1.2.3.4 and port 99", device="any", revports=True)

# collect terminated thread
th.join()


# do the same but resend it to a new destination
th = SendPacket(packet, 2)
th.start()
models.react(2, filter="host 1.2.3.4 and port 99", device="any",
            revports=True, forward="67.205.14.183")
th.join()
