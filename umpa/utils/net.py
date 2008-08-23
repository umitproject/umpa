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
This module contains some functions related to network issues.
"""

def _pieces_of_number(number, piece_size=8):
    """
    Return list of the number pieces.
    
    @type number: C{int}
    @param number: the number for splitting.

    @type piece_size: C{int}
    @param piece_size: size of the each piece (default: 8 bits)

    @rtype: C{list}
    @return: the number pieces.
    """

    ret = []
    mask = 2**piece_size - 1
    while number:
        ret.append(number & mask)
        number >>= piece_size
    ret.reverse()
    return ret

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

    pieces = _pieces_of_number(data)
    if len(pieces)%2 == 1:
        pieces.append(0)

    for i in xrange(0, len(pieces), 2):
        x = ((pieces[i] << 8) & 0xff00) + (pieces[i+1] & 0xff)
        cksum += x

    while cksum >> 16:
        cksum = (cksum & 0xffff) + (cksum >> 16)

    cksum = ~cksum
    return int(cksum & 0xffff)
