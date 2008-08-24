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
Functions related with parsing bits of numbers.
"""

BYTE = 8

def split_into_chunks(number, number_length, chunks_size=BYTE):
    """
    Split the big number into small chunks.

    The number_length argument isn't odd as you may think in the first time.
    We could calculte it but what if the number is 10 (4 bits) but the number
    length should be 32 bits? That why, number_length is necessary.
    
    @type number: C{int}
    @param number: the number which will be splitted.

    @type number_length: C{int}
    @param number_length: length of the number in bits

    @type chunks_size: C{int}
    @param chunks_size: size of the single chunk (default: 8 (1 byte) )

    @rtype: C{int}
    @return: splitted chunks.
    """
    
    mask = 2**chunks_size - 1
    bytes = number_length / chunks_size
    return [ (number & (mask << (chunks_size*i))) >> chunks_size*i
                                    for i in reversed(xrange(bytes)) ]

def get_bits(number, bits, offset=0, rev_offset=False):
    """
    Return n bits from the number ragarding to offset.
    
    By default offset is from the left side.
    It is recommended to use right side offset (works much faster).

    @type number: C{int}
    @param number: the number which will be parsed.

    @type bits: C{int}
    @param bits: number of bits for the return

    @type offset: C{int}
    @param offset: offset of the bits (default: 0)

    @type rev_offset: C{bool}
    @param rev_offset: a direction of the offset (default: from left to right).

    @rtype: C{int}
    @return: grabbed n bits from the number
    """

    if not rev_offset:
        length = 0
        while number >= 2**length:
            length += 1
        offset = length - offset - bits
    return (number & (2**bits-1 << offset)) >> offset
