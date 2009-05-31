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

import pcap
import py.test

import umpa
from umpa.protocols import IP, TCP
from umpa.sniffing.libpcap import pypcap
from umpa.utils.exceptions import UMPASniffingException
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

    def test_openlive(self):
        try:
            obj = pypcap.open_live()
            assert obj.device == pcap.lookupdev()
            obj = pypcap.open_live(device="any") # XXX can we use 'any'?
            assert obj.device == "any"
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")

    def test_findalldevs(self):
        try:
            assert pypcap.findalldevs() == pcap.findalldevs()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")

    def test_loop_and_filter(self):
        # XXX it would rather looped than failing
        def cbk(timestamp, pkt, *args):
            assert args[0] == "foobar" # stupid isn't it? :)

        try:
            p = pypcap.open_live("any", to_ms=100)
            p.setfilter("src host 1.2.3.4 and src port 99")
            th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                        TCP(source_port=99)))
            th.start()
            p.loop(1, cbk, "foobar")
            th.join()

            th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                        TCP(source_port=99)), 5)
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
        th = SendPacket(umpa.Packet(IP(source_address="1.2.3.4"),
                                    TCP(source_port=99)), amount)
        th.start()
        try:
            p = pypcap.open_live("any", to_ms=100)
            p.setfilter("src host 1.2.3.4 and src port 99")
            for i in xrange(amount):
                packet = p.next()
        except UMPASniffingException:
            py.test.skip("no suitable devices for sniffing found. "
                        "propably not sufficent priviliges.")
        finally:
            th.join()
