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

import sys
import tempfile

import pcap
import py.test

import umit.umpa
from umit.umpa.protocols import IP, TCP
from umit.umpa.sniffing.libpcap import pypcap
from umit.umpa.utils.exceptions import UMPASniffingException
from tests.utils import SendPacket

class TestPypcap(object):
    # tests are tivial...but it's a wrapper, right?
    # TODO: test_dispatch()
    def test_lookupdev(self):
        try:
            pcap.lookupdev()
        except OSError:
            py.test.raises(UMPASniffingException, pypcap.lookupdev)
        else:
            assert pypcap.lookupdev() == pcap.lookupdev()

    def test_findalldevs(self):
        try:
            assert pypcap.findalldevs() == pcap.findalldevs()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")

    def test_lookupdev_findall(self):
        # current pypcap shows diffent names for findalldevs() and lookupdev()
        # under windows, so skip it
        if sys.platform.find('win') != -1:
            py.test.skip("not supported by windows")

        assert pcap.lookupdev() in pcap.findalldevs()

class TestOpenPcap(object):
    def test_openlive(self):
        try:
            obj = pypcap.open_pcap()
            assert obj.device == pcap.lookupdev()
            obj = pypcap.open_pcap(device="any") # XXX can we use 'any'?
            assert obj.device == "any"
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")

    def test_loop_and_filter(self):
        # XXX it would rather looped than failing
        def cbk(timestamp, pkt, *args):
            assert args[0] == "foobar" # stupid isn't it? :)

        try:
            p = pypcap.open_pcap("any", to_ms=100)
            p.setfilter("src host 1.2.3.4 and src port 99")
            th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                        TCP(srcport=99)))
            th.start()
            p.loop(1, cbk, "foobar")
            th.join()

            th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                        TCP(srcport=99)), 5)
            th.start()
            p.loop(5, cbk, "foobar")
            th.join()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")

    def test_next(self):
        # can't test iterable of the object
        # because pypcap doesn't raise StopIteration
        amount = 5
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)), amount)
        th.start()
        try:
            p = pypcap.open_pcap("any", to_ms=100)
            p.setfilter("src host 1.2.3.4 and src port 99")
            for i in xrange(amount):
                packet = p.next()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")
        finally:
            th.join()

class TestDumper(object):
    def test_dump(self):
        amount = 5
        dump_file = tempfile.NamedTemporaryFile(mode="w")
        th = SendPacket(umit.umpa.Packet(IP(src="1.2.3.4"),
                                    TCP(srcport=99)), amount)
        th.start()
        try:
            p = pypcap.open_pcap("any", to_ms=100)
            p.setfilter("src host 1.2.3.4 and src port 99")
            d = pypcap.dumper()
            d.open(p, dump_file.name)
            pkts = []
            for i in xrange(amount):
                pkts.append(p.next())
                d.dump()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")
        finally:
            th.join()
        d.close()
        p = pypcap.open_pcap(dump_file.name)
        p.setfilter("src host 1.2.3.4 and src port 99")
        for i, pkt in enumerate(p):
            assert pkt[0] == pkts[i][0]
            # not sure if the below should be equivalent
            assert str(pkt[1]) == str(pkts[i][1])
