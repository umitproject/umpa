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

import tempfile

import umit.umpa
import umit.umpa.sniffing
from umit.umpa.protocols import IP, TCP
from umit.umpa.protocols._decoder import decode
from umit.umpa.utils.exceptions import UMPASniffingException
from tests.utils import SendPacket

import py.test

class TestSniffing(object):
    def test_import_backend(self):
        assert hasattr(umit.umpa.sniffing, 'lpcap')
        assert umit.umpa.sniffing.lpcap._backend == umit.umpa.config['libpcap']

        oldlpcap = umit.umpa.config['libpcap']
        umit.umpa.config['libpcap'] = "foobar"
        py.test.raises(UMPASniffingException, "reload(umit.umpa.sniffing)")
        umit.umpa.config['libpcap'] = oldlpcap

    def test_get_available_devices(self):
        if umit.umpa.config['libpcap'] == 'pypcap':
            from umit.umpa.sniffing.libpcap import pypcap
            assert umit.umpa.sniffing.get_available_devices()==pypcap.findalldevs()

    def test_sniff(self):
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)))
        th.start()
        result = umit.umpa.sniffing.sniff(1, device='any', filter="src port 99")
        th.join()

        assert len(result) == 1
        assert result[0].ip.src == '1.2.3.4'
        assert result[0].tcp.srcport == 99

    def test_sniff_next(self):
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)))
        th.start()
        result = umit.umpa.sniffing.sniff_next(device='any', filter="src port 99")
        th.join()

        assert result.ip.src == '1.2.3.4'
        assert result.tcp.srcport == 99

        # send more, sniff one
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)), 5)
        th.start()
        result = umit.umpa.sniffing.sniff_next(device='any', filter="src port 99")
        th.join()

        assert result.ip.src == '1.2.3.4'
        assert result.tcp.srcport == 99


    def test_sniff_loop(self):
        def cbk(ts, pkt, *args):
            assert pkt.ip.src == "1.2.3.6"
            assert pkt.tcp.srcport == 99
            assert ts > 0
            assert len(args) == 2
            if args[0] > args[1]:
                raise UMPASniffingException("test")

        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.6"),
                                    TCP(srcport=99)), 2)
        th.start()
        umit.umpa.sniffing.sniff_loop(1, filter="src 1.2.3.6", device='any',
                                            callback=cbk, callback_args=[1,2])
        th.join()

        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.6"),
                                    TCP(srcport=99)))
        th.start()
        py.test.raises(UMPASniffingException, umit.umpa.sniffing.sniff_loop, 1,
                        filter="src 1.2.3.6", device='any', callback=cbk,
                        callback_args=[2,1] )
        th.join()

        py.test.raises(UMPASniffingException, umit.umpa.sniffing.sniff_loop, 1)

    def test_from_file(self):
        dump_file = tempfile.NamedTemporaryFile(mode="w")
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.6"),
                                    TCP(srcport=99)), 3)
        th.start()
        umit.umpa.sniffing.sniff(3, device="any", dump=dump_file.name,
                            filter="src host 1.2.3.6 and src port 99")
        th.join()

        result = umit.umpa.sniffing.from_file(dump_file.name)

        assert len(result) == 3
        for packet in result:
            assert packet.ip.src == "1.2.3.6"
            assert packet.tcp.srcport == 99

        result = umit.umpa.sniffing.from_file(dump_file.name, 2)
        assert len(result) == 2
        for packet in result:
            assert packet.ip.src == "1.2.3.6"
            assert packet.tcp.srcport == 99


    def test_from_file_loop(self):
        global idx
        idx = 0
        def cbk(ts, pkt, *args):
            global idx
            assert pkt.ip.src == "1.2.3.6"
            assert pkt.tcp.srcport == 99
            assert ts > 0
            assert len(args) == 1
            idx += 1

        dump_file = tempfile.NamedTemporaryFile(mode="w")
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.6"),
                                    TCP(srcport=99)), 3)
        th.start()
        umit.umpa.sniffing.sniff(3, device="any", dump=dump_file.name,
                            filter="src host 1.2.3.6 and src port 99")
        th.join()

        idx = 0
        amount = 3
        umit.umpa.sniffing.from_file_loop(dump_file.name, callback=cbk,
                                    callback_args=[amount,])
        assert idx == amount

        idx = 0
        amount = 2
        umit.umpa.sniffing.from_file_loop(dump_file.name, 2, callback=cbk,
                                            callback_args=[amount,])
        assert idx == amount

    def test_to_file(self):
        dump_file = tempfile.NamedTemporaryFile(mode="w")
        amount = 5

        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)), amount)
        th.start()
        try:
            umit.umpa.sniffing.to_file(dump_file.name, amount,
                    "src host 1.2.3.4 and src port 99", "any")
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")
        finally:
            th.join()

        result = umit.umpa.sniffing.from_file(dump_file.name)
        assert len(result) == amount
        for packet in result:
            assert packet.ip.src == "1.2.3.4"
            assert packet.tcp.srcport == 99

        result = umit.umpa.sniffing.from_file(dump_file.name, 2)
        assert len(result) == 2
        for packet in result:
            assert packet.ip.src == "1.2.3.4"
            assert packet.tcp.srcport == 99
