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

import umpa
import umpa.sniffing
from umpa.protocols import IP, TCP
from umpa.utils.exceptions import UMPASniffingException
from tests.utils import SendPacket

import py.test

class TestSniffing(object):
    def test_import_backend(self):
        assert hasattr(umpa.sniffing, 'lpcap')
        assert umpa.sniffing.lpcap._backend == umpa.config['libpcap']

        oldlpcap = umpa.config['libpcap']
        umpa.config['libpcap'] = "foobar"
        py.test.raises(UMPASniffingException, "reload(umpa.sniffing)")
        umpa.config['libpcap'] = oldlpcap

    def test_get_available_devices(self):
        if umpa.config['libpcap'] == 'pypcap':
            from umpa.sniffing.libpcap import pypcap
            assert umpa.sniffing.get_available_devices()==pypcap.findalldevs()

    def test_sniff(self):
        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                    TCP(source_port=99)))
        th.start()
        result = umpa.sniffing.sniff(1, device='any')
        th.join()
        print result

    def test_sniff_next(self):
        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                    TCP(source_port=99)))
        th.start()
        result = umpa.sniffing.sniff_next(device='any')
        th.join()
        print result

        # send more, sniff one
        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                    TCP(source_port=99)), 5)
        th.start()
        result = umpa.sniffing.sniff_next(device='any')
        th.join()
        print result


    def test_sniff_loop(self):
        def cbk(ts, pkt, *args):
            # XXX it's stupid. should be rewritten when full sniffing
            # will be available
            print pkt
            if args[0] > args[1]:
                raise UMPASniffingException("test")

        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.6"),
                                    TCP(source_port=99)))
        th.start()
        umpa.sniffing.sniff_loop(1, filter="src 1.2.3.6", device='any',
                                            callback=cbk, callback_args=[1,2])
        th.join()

        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.6"),
                                    TCP(source_port=99)))
        th.start()
        py.test.raises(UMPASniffingException, umpa.sniffing.sniff_loop, 1,
                        filter="src 1.2.3.6", device='any', callback=cbk,
                        callback_args=[2,1] )
        th.join()
