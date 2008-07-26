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

def in_cksum(data, sum=0):
    """Return internet checksum.

    It is an implementation of RFC 1071.
    """
    l = len(data)
    for i in xrange(0, l, 2):
        if i + 1 >= l:
            cksum += ord(data[i]) & 0xff
        else:
            x = ((ord(data[i]) << 8) & 0xff00) + (ord(data[i+1]) & 0xff)
            cksum += x

    while (cksum >> 16) > 0:
        cksum = (cksum & 0xffff) + (cksum >> 16)

    cksum = ~cksum
    return cksum & 0xffff
