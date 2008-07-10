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

from my_exceptions import UMPAException

def _pairwise(iterable):
    itnext = iter(iterable).next
    while True:
        yield itnext(), itnext()

def dict_from_sequence(seq):
    """Return a dictionary based on a sequence."""
    return dict(_pairwise(seq))

def get_item_by_name(seq, seq_with_name, name):
    """Return an item from the sequence based on the another sequence
    and position of the name there.
    """
    return seq[seq_with_name.index(name)]
