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
from umit.umpa.protocols import ICMPV6
from umit.umpa.utils.exceptions import UMPAException, UMPAAttributeException

def raw(obj):
    return obj._raw(0, 0, [obj], 0)

class TestICMPV6(object):

    def test_active_fields(self):
        """
        test if the active fields are set properly for supported ICMPV6 types
        """

        i = ICMPV6()
        # default - no type
        for name in ( 'ident', 'seq','pointer','mtu',
                      'cur_limit','m','o','reserverd','life_time','r','s','o_na',
                      'reachable_time','retrans_time','reserved_na','ip_addr' ,'target_addr','dest_addr' ):
            assert i.get_field(name).active == False
        for name in ( 'unused', 'data', ):
            assert i.get_field(name).active == True
        
        for type in ( 128,129 ):
            i.type = type
            for name in ( 'pointer','mtu','cur_limit','m','o','reserverd','life_time',
                          'r','s','o_na','reachable_time','retrans_time','reserved_na','ip_addr', 'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'ident', 'seq', ):
                assert i.get_field(name).active == True
                
        for type in ( 4 ,):
            i.type = type
            for name in ( 'ident', 'seq','mtu','cur_limit','m','o','reserverd','life_time',
                          'r','s','o_na','reachable_time','retrans_time','reserved_na','ip_addr', 'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'pointer', ):
                assert i.get_field(name).active == True
                

        for type in ( 2,):
            i.type = type
            for name in ( 'ident', 'seq','pointer','cur_limit','m','o','reserverd','life_time',
                          'r','s','o_na','reachable_time','retrans_time','reserved_na','ip_addr', 'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'mtu', ):
                assert i.get_field(name).active == True

        for type in ( 134 ,):
            i.type = type
            for name in ( 'ident', 'seq','pointer',
                          'r','s','o_na','reserved_na','ip_addr' ,'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'cur_limit','m','o','reserverd','life_time','reachable_time','retrans_time', ):
                assert i.get_field(name).active == True    


        for type in ( 135,):
            i.type = type
            for name in ( 'ident', 'seq','pointer','cur_limit','m','o','reserverd','life_time',
                          'r','s','o_na','reachable_time','retrans_time','reserved_na','mtu' ,'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'ip_addr', ):
                assert i.get_field(name).active == True      
                

        for type in ( 136,):
            i.type = type
            for name in ( 'ident', 'seq','pointer','mtu','cur_limit','m','o','reserverd','life_time',
                          'reachable_time','retrans_time' ,'target_addr','dest_addr'):
                assert i.get_field(name).active == False
            for name in ( 'r','s','o_na','reserved_na','ip_addr', ):
                assert i.get_field(name).active == True 

        for type in ( 137,):
            i.type = type
            for name in ( 'ident', 'seq','pointer','mtu','cur_limit','m','o','reserverd','life_time',
                          'r','s','o_na','reserved_na','ip_addr','reachable_time','retrans_time'):
                assert i.get_field(name).active == False
            for name in (  'target_addr','dest_addr', ):
                assert i.get_field(name).active == True 

    def test_load_raw(self):
        i = ICMPV6()

        # code
        i.load_raw("\x00\x42\xbd\xff\x00\x00\x00\x00")
        assert i.type == 0
        assert i.code == 0x42

        
        i.load_raw("\x80\x00\x92\x84\x12\x34\x56\x78\x41\x42\x43\x44")
        assert i.type == 128
        assert i.code == 0
        assert i._checksum == 0x9284
        assert i.ident == 0x1234
        assert i.seq == 0x5678
        assert i.data == 'ABCD'
        
        
        i.load_raw("\x04\x00\x92\x84\x12\x34\x56\x78\x41\x42\x43\x44")
        assert i.type == 4
        assert i.code == 0
        assert i._checksum == 0x9284
        assert i.pointer == 0x12345678
        assert i.data == 'ABCD'
        
        i.load_raw("\x02\x00\x92\x84\x12\x34\x56\x78\x41\x42\x43\x44")
        assert i.type == 2
        assert i.code == 0
        assert i._checksum == 0x9284
        assert i.mtu == 0x12345678
        assert i.data == 'ABCD' 
        
        i.load_raw("\x86\x00\x92\x84\x12\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12")
        assert i.type == 134
        assert i.code == 0
        assert i._checksum == 0x9284
        assert i.cur_limit == 18
        assert i.m == 1
        assert i.o == 0
        assert i.reserverd == 52
        assert i.life_time == 22136
        assert i.reachable_time == 267560
        assert i.retrans_time == 427026
        
        i.load_raw("\x87\x00\x92\x84\x12\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12\x92\x84\x12\xB4\x56\xB4\x56\x78")
        assert i.type == 135
        assert i.code == 0
        assert i._checksum == 0x9284
        assert i.unused == 313808504
        assert i.ip_addr == '0004:1528:0006:8412:9284:12b4:56b4:5678'  
        
        i.load_raw("\x88\x00\x92\x84\xB2\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12\x92\x84\x12\xB4\x56\xB4\x56\x78")
        assert i.type == 136
        assert i.code == 0
        assert i._checksum == 0x9284 
        assert i.r == 1
        assert i.s == 0
        assert i.o_na == 1 
        assert i.reserved_na == 313808504
        assert i.ip_addr == '0004:1528:0006:8412:9284:12b4:56b4:5678' 
        
        
        i.load_raw("\x89\x00\x92\x84\xB2\xB4\x56\x78\x00\x04\x15\x28\x00\x06\x84\x12\x92\x84\x12\xB4\x56\xB4\x56\x78\x80\x04\x16\x28\x03\x06\x84\x12\x02\x84\x14\xB4\x53\xB4\x56\x78")
        assert i.type == 137
        assert i.code == 0
        assert i._checksum == 0x9284 
        assert i.unused == 2998163064L
        assert i.target_addr == '0004:1528:0006:8412:9284:12b4:56b4:5678'
        assert i.dest_addr == '8004:1628:0306:8412:0284:14b4:53b4:5678'  
        
                                                                       
