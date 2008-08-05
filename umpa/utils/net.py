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

def _pieces_of_number(number, piece_size=8):
    """Return list of pieces of the number.
    
    Number is divided on piece_size bits.
    Default is 8bits.
    """

    ret = []
    mask = 2**piece_size - 1
    while number:
        ret.append(number & mask)
        number >>= piece_size
    ret.reverse()
    return ret

def in_cksum(data, cksum=0):
    """Return Internet Checksum.

    It is an implementation of RFC 1071.

    To check if checksum is correct pass it as cksum argument.
    If the result is 0, then the ckecksum has not detected an error.
    """

    pieces = _pieces_of_number(data)
    for i in xrange(0, len(pieces), 2):
        if i + 1 == len(pieces):
            cksum += pieces[i] & 0xff
        else:
            x = ((pieces[i] << 8) & 0xff00) + (pieces[i+1] & 0xff)
            cksum += x

    while cksum >> 16:
        cksum = (cksum & 0xffff) + (cksum >> 16)

    cksum = ~cksum
    return int(cksum & 0xffff)
