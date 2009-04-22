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
Functions related with parsing bits of numbers.
"""

from umpa.utils.exceptions import UMPAException

BYTE = 8

def split_number_into_chunks(number, chunk_size=BYTE, chunk_amount=None):
    """
    Split the big number into small chunks.
    
    @type number: C{int}
    @param number: the number for splitting.

    @type chunk_size: C{int}
    @param chunk_size: size of the each chunk (default: 8 bits)

    @rtype: C{list}
    @return: list of chunks.
    """

    chunks = []
    mask = 2**chunk_size - 1
    while number:
        chunks.append(number & mask)
        number >>= chunk_size

    if chunk_amount is not None:
        extend_zero = chunk_amount - len(chunks)
        if extend_zero < 0:
            raise UMPAException("Wrong amount of requested chunks. Requested "
                                "%d, minimum %d." % (chunk_amount,len(chunks)))
        chunks.extend([0]*extend_zero)

    chunks.reverse()
    return chunks

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
