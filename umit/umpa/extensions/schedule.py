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
Schedule feature is for sending packets.

2 features are provided:
 1. delay before start sending
 2. interval before each packet

send() function is provided and new method
for umit.umpa.Socket objects is added.
"""

import time
import threading

import umit.umpa
from umit.umpa.utils.exceptions import UMPAException

def _sleep(delay):
    """
    Call system sleep() function.

    @type delay: C{int}
    @param delay: time in seconds for the sleeping.
    """

    time.sleep(delay)

def _send_packets(packets, delay, interval, socket):
    # delay before start
    _sleep(delay)
    sent_bits = []
    for packet in packets:
        sent_bits.append(socket.send(packet))
        if interval:
            _sleep(interval)
    return sent_bits

class _DetachThread(threading.Thread):
    def __init__(self, delay, packets, interval, socket):
        super(DetachThread, self).__init__()
        self._delay = delay
        self._packets = packets
        self._interval = interval
        self._socket = socket

    def run(self):
        _send_packets(self._delay, self._packets, self._interval, self._socket)


def send(delay, packets=None, *args, **kwargs):
    """
    Send packets with the delay,

    @type delay: C{int}
    @param delay: delay before first sending.

    @type packets: C{Packet}
    @param packets: list of packets for sending.

    @type args: C{Packet}
    @param args: additional list of packets for sending.

    @param kwargs: extra options, currently available are:
      - detach - send packets in the background (B{type}: C{bool})
      - interval - set interval between packets (B{type}: C{int}),
      - socket - use passed socket, otherwise create new umit.umpa.Socket()
        object (B{type}: C{umit.umpa.Socket})

    @rtype: C{list}
    @return: sent bits of each packet (@note: only if detach=False).
    """
    # parsing passed options
    options = { 'detach'    : False,
                'interval'  : None,
                'socket'    : umit.umpa.Socket(),
                }
    for opt in kwargs:
        if opt not in options:
            raise UMPAException("Undefined option " + opt)
        else:
            options[opt] = kwargs[opt]

    # merge packets
    if packets is None:
        packets = []
    try:
        packets = list(packets)
    except TypeError:
        packets = [packets]
    packets.extend(args)

    # use threads if detach
    if options['detach']:
        t = _DetachThread(packets, delay, options['interval'], options['socket'])
        t.start()
    else:
        return _send_packets(packets, delay, options['interval'], options['socket'])

def _send_schedule(self, delay, *packets, **options):
    """
    Send packets with some delays (initial, interval).

    @type delay: C{int}
    @param delay: delay before first sending.

    @type packets: C{Packet}
    @param packets: list of packets for sending.

    @param options: extra options, currently available are:
      - detach - send packets in the background (B{type}: C{bool})
      - interval - set interval between packets (B{type}: C{int}),
      - socket - use passed socket, otherwise create new umit.umpa.Socket()
        object (B{type}: C{umit.umpa.Socket})

    @rtype: C{list}
    @return: sent bits of each packet.
    """

    return send(delay, socket=self, *packets, **options)

umit.umpa.Socket.send_schedule = _send_schedule
