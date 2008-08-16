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

BYTE = 8

def split_into_chunks(number, number_length, chunks_size=BYTE):
    """Split the big number into small chunks (default BYTE size).
    Return them as a list.
    """
    mask = 2**chunks_size - 1
    bytes = number_length / chunks_size
    return [ (number & (mask << (chunks_size*i))) >> chunks_size*i
                                    for i in reversed(xrange(bytes)) ]

def get_bits(number, bits, offset=0, rev_offset=False):
    """Return n bits from the number ragarding to offset.
    
    By default offset is from the left side.
    It is recommended to use right side offset (works much faster).
    """
    if not rev_offset:
        length = 0
        while number >= 2**length:
            length += 1
        offset = length - offset - bits
    return (number & (2**bits-1 << offset)) >> offset
