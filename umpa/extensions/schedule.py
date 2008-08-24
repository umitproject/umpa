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
Schedule feature for the sending packets.

2 features are provided:
 1. delay before start sending
 2. interval before each packet

send() function is provided and new method for umpa.Socket objects is added.

@attention: This extension works in blocking-way. The main process is being
blocked during delays. It will be rewritten in the asynchronous way soon.
Be patient.
"""

import time

import umpa

def _sleep(delay):
    """
    Call system sleep() function.

    @type delay: C{int}
    @param delay: time in seconds for the sleeping.
    """

    time.sleep(delay)

def send(delay, *packets, **options):
    """
    Send packets with the delay,

    @type delay: C{int}
    @param delay: delay before first sending.

    @type packets: C{Packet}
    @param packets: list of packets for sending.

    @param options: extra options, currently available are:
      - detach - send packets in the background (B{type}: C{bool})
        (not implemented yet),
      - interval - set interval between packets (B{type}: C{int}),
      - socket - use passed socket, otherwise create new umpa.Socket() object
        (B{type}: C{umpa.Socket})

    @rtype: C{list}
    @return: sent bits of each packet.
    """

    # parsing options
    if "detach" in options:
        # TODO: The only reasonable way to implement this feature
        # is to use asynch way.
        # spawning processes or threading are totally bad for a library
        # but to write it with select() we need a bit more time, but
        # it worth to wait for it than using threads etc.
        raise NotImlementedError("It will be implemented soon. Sorry!")
        detach = int(options['detach'])
    else:
        detach = False

    if "interval" in options:
        interval = int(options['interval'])
    else:
        interval = None

    if "socket" in options:
        sock = options["socket"]
    else:
        sock = umpa.Socket()

    sent_bits = []

    # forking if detach
    if detach:
        pass

    # delay before start
    _sleep(delay)

    for packet in packets:
        sent_bits.append(sock.send(packet))
        if interval:
            _sleep(interval)

    return sent_bits

def _send_schedule(self, delay, *packets, **options):
    """
    Send packets with some delays (initial, interval).

    @type delay: C{int}
    @param delay: delay before first sending.

    @type packets: C{Packet}
    @param packets: list of packets for sending.

    @param options: extra options, currently available are:
      - detach - send packets in the background (B{type}: C{bool})
        (not implemented yet),
      - interval - set interval between packets (B{type}: C{int}),
      - socket - use passed socket, otherwise create new umpa.Socket() object
        (B{type}: C{umpa.Socket})

    @rtype: C{list}
    @return: sent bits of each packet.
    """

    return send(delay, socket=self, *packets, **options)

umpa.Socket.send_schedule = _send_schedule
