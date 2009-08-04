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
Functions related to network issues.
"""

import umit.umpa.utils.bits

def in_cksum(data, cksum=0):
    """
    Return Internet Checksum.

    It is an implementation of RFC 1071.

    To check if the already calculated checksum is correct, pass it as cksum
    argument. If the result is 0, then the ckecksum has not detected an error.

    @type data: C{int}
    @param data: the data from which checksum is calculated.

    @type cksum: C{int}
    @param cksum: already calculated checksum for comparision (default: 0)

    @rtype: C{int}
    @return: calculated checksum.
    """

    pieces = umit.umpa.utils.bits.split_number_into_chunks(data)
    if len(pieces)%2 == 1:
        pieces.append(0)

    for i in xrange(0, len(pieces), 2):
        xxx = ((pieces[i] << 8) & 0xff00) + (pieces[i+1] & 0xff)
        cksum += xxx

    while cksum >> 16:
        cksum = (cksum & 0xffff) + (cksum >> 16)

    cksum = ~cksum
    return int(cksum & 0xffff)

def parse_ipv4(ip):
    """
    Return 4 numbers of an IPv4
    
    192.168.1.2 -> [192, 168, 1, 2]

    @type ip: C{str}
    @param ip: the ip to parse.

    @rtype: C{int}
    @return: 4 numbers.
    """
    return [ int(x) for x in ip.split('.') ]
