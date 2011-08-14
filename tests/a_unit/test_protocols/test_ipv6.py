#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Adriano Monteiro Marques.
#
# Author: Gaurav Ranjan < g.ranjan143@gmail.com>
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
from umit.umpa.protocols import IPV6
from umit.umpa.utils.exceptions import UMPAException, UMPAAttributeException

def raw(obj):
    return obj._raw(0, 0, [obj], 0)

class TestICMPV6(object):

    def test_get_raw(self):
        """
        test if the get raw are calculated properly
        """

        raw_val = raw(IPV6(src = '0000:0000:0000:0000:0000:0000:0000:0001', dst = '0000:0000:0000:0000:0000:0000:0000:0001' ))
        assert raw_val == (800995138470341488281764963846888046591648346443787753937023421462503530299736539038457735938049L, 320)
        
        raw_val = raw(IPV6(src = '0000:0000:0000:0000:0000:0000:0000:0001', dst = '0000:0000:0000:0000:0000:0000:0000:0001' , _hop_limit = 52))
        assert raw_val == (800995138470341464775970848671700375606738389680142459723216534337469030289846985432092419031041L, 320)
        
        raw_val = raw(IPV6(src = '0000:0000:0000:0000:0000:0000:0000:0001', dst = '0000:0000:0000:0000:0000:0000:0000:0001' , _hop_limit = 52 , _nxt_hdr = 6 ))
        assert raw_val == (800995138470341464775970848671700375606738389680142459723216534337469030289846985432092419031041L, 320)

        raw_val = raw(IPV6(src = '0000:0000:0000:0000:0000:0000:0000:0001', dst = '0000:0000:0000:0000:0000:0000:0000:0001' , _hop_limit = 52 , _nxt_hdr = 6 ,_flow_label = 31 ))
        assert raw_val == (800995153887361793479356755488550068158184432794283134440995774991852313977791392820627060555777L, 320)

        raw_val = raw(IPV6(src = '0004:1528:0006:8412:9284:12b4:56b4:5678', dst = '8004:1628:0306:8412:0284:14b4:53b4:5678' ))
        assert raw_val == (800995138470341488281772177250220989906070022452923989020537361779717712177802081057211329828472L, 320)
        
        raw_val = raw(IPV6(src = '0004:1528:0006:8412:9284:12b4:56b4:5678', dst = '8004:1628:0306:8412:0284:14b4:53b4:5678' , _hop_limit = 52))
        assert raw_val == (800995138470341464775978062075033318921160065689278694806730474654683212167912527450846012921464L, 320)
        
        raw_val = raw(IPV6(src = '0004:1528:0006:8412:9284:12b4:56b4:5678', dst = '8004:1628:0306:8412:0284:14b4:53b4:5678' , _hop_limit = 52 , _nxt_hdr = 6 ))
        assert raw_val == (800995138470341464775978062075033318921160065689278694806730474654683212167912527450846012921464L, 320)

        raw_val = raw(IPV6(src = '0004:1528:0006:8412:9284:12b4:56b4:5678', dst = '8004:1628:0306:8412:0284:14b4:53b4:5678' , _hop_limit = 52 , _nxt_hdr = 6 ,_flow_label = 31 ))
        assert raw_val == (800995153887361793479363968891883011472606108803419369524509715309066495855856934839380654446200L, 320)

    def test_load_raw(self):
        
        i = IPV6()

        # code
        i.load_raw("\x88\x00\x92\x84\xB2\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12\x92\x84\x12\xB4\x56\xB4\x56\x78\x80\x04\x16\x28\x03\x06\x84\x12\x02\x84\x14\xB4\x53\xB4\x56\x78")
        assert i._version == 8
        assert i.dscp == 32
        assert i.ds == 0
        assert i._flow_label == 37508
        assert i._payload == 45748
        assert i._nxt_hdr == 86
        assert i._hop_limit == 120 
        assert i.src == '0004:1528:0006:8412:9284:12b4:56b4:5678'
        assert i.dst == '8004:1628:0306:8412:0284:14b4:53b4:5678' 
        
                                                               
