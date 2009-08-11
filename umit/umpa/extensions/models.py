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

"""
Useful functions to make life easier.

This extension doesn't provide anything new what you can't do by your own.
But it provides some functions which are used often so using it can decrease
time for coding.
"""

import umit.umpa
from umit.umpa.sniffing import sniff_next
from umit.umpa.utils.exceptions import UMPAException

def react(count, forward=None, filter=None, device=None, timeout=0,
            snaplen=1024, promisc=True, **kwargs):
    """
    Sniff and resend packets with some reaction.

    Sniffed packet can be modify (e.g. by reversing src/dst ports) and resend.

    For description of arguments please see umit.umpa.sniffing package.
    Available reactions:
     1. revhosts -- revert hosts
     2. revports -- revert ports
     3. forward  -- forward packet to a new destination
    To set reactions use dict-style keywords like revhosts=True.
    """

    def revhosts(pkt):
        tmp = pkt.ip.dst
        pkt.ip.dst = pkt.ip.src
        pkt.ip.src = tmp
        return pkt

    def revports(pkt):
        for proto in pkt.protos:
            if proto.layer == 4:
                tmp = proto.dstport
                proto.dstport = proto.srcport
                proto.srcport = tmp
                break
        return pkt

    def forwardfunc(pkt, fwd):
        pkt.ip.dst = fwd
        return pkt

    avail_opts = ('revports', 'revhosts',)

    for opt in kwargs:
        if opt not in avail_opts:
            raise UMPAException("Undefined option " + opt)

    options = {}
    for opt in avail_opts:
        options[opt] = kwargs.get(opt)

    sock = umit.umpa.Socket()
    for i in xrange(count):
        pkt = sniff_next(filter=filter, device=device, timeout=timeout,
                        snaplen=snaplen, promisc=promisc)
        for opt in options:
            if options[opt] is True:
                pkt = locals()[opt](pkt)
        if forward is not None:
            pkt = forwardfunc(pkt, forward)
        # remove 2nd layer
        while pkt.protos[0].layer < 3:
            pkt.protos.pop(0)
        sock.send(pkt)
