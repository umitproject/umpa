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

import py.test
from umpa.utils.bits import *

class TestUtilBitsGet(object):
    def test_get_bits(self):
        assert get_bits(10, 2) == 2
        assert get_bits(666666, 3) == 5
        assert get_bits(666666, 3, 1) == 2
        assert get_bits(666666, 3, rev_offset=True) == 2
        assert get_bits(999999999999999, 9) == 454
        assert get_bits(999999999999999, 9, 9) == 382
        assert get_bits(999999999999999, 9, 9, True) == 319

    def test_get_bits_errors(self):
        py.test.raises(ValueError, get_bits, 0, 1)
        py.test.raises(ValueError, get_bits, 10, 100)

class TestUtilBitsChunks(object):
    def test_chunks(self):
        assert split_number_into_chunks(0xFFFF) == [0xFF, 0xFF]
        assert split_number_into_chunks(0xFFFF, 16) == [0xFFFF]
        assert split_number_into_chunks(0xFFFFF) == [0xF, 0xFF, 0xFF]
        assert split_number_into_chunks(0xFFFFF,4) == [0xF, 0xF, 0xF, 0xF, 0xF]
        assert split_number_into_chunks(0xFFFFF, 5) == [0x1F, 0x1F, 0x1F, 0x1F]

    def test_amount(self):
        assert split_number_into_chunks(0xFFFF,chunk_amount=3) == [0,0xFF,0xFF]
        assert split_number_into_chunks(0xFFFF, 16, 2) == [0, 0xFFFF]

        py.test.raises(UMPAException, split_number_into_chunks, 0xF, 1, 1)
