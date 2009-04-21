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
Functions which are not clasified in other categories.
"""

def _pairwise(iterable):
    """
    Generate pair (key, value) from the iterable sequence.

    @type iterable: any iterable object
    @param iterable: the sequence of pairs alternately keys, values.
    """

    itnext = iter(iterable).next
    while True:
        yield itnext(), itnext()

def dict_from_sequence(seq):
    """
    Return a dictionary based on the sequence.

    A dictionary is built from the pairs of key and value from the sequence.
    Example of the sequence:
    seq = [key1, value1, key2, value2]

    @type seq: any iterable object
    @param seq: the sequence which will be converted to the dictionary.

    @rtype: C{dict}
    @return: a dictionary based on the sequence.
    """
    
    return dict(_pairwise(seq))
