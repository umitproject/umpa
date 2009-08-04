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

import Queue
import threading

import umpa
import umpa.sniffing
from umpa.protocols import IP, TCP
from umpa.extensions import models
from umpa.utils.exceptions import UMPAException
from tests.utils import SendPacket

import py.test

class SniffThread(threading.Thread):
    def __init__(self, filter, device, queue):
        super(SniffThread, self).__init__()
        self._filter = filter
        self._device = device
        self._queue = queue

class RevPortsThread(SniffThread):
    def run(self):
        pkt = umpa.sniffing.sniff(2, device=self._device, filter=self._filter)
        try:
            assert pkt[0].ip.src == "127.0.0.1"
            assert pkt[0].ip.dst == "127.0.0.1"
            assert pkt[0].tcp.srcport == 80
            assert pkt[0].tcp.dstport == 0
            assert pkt[1].ip.src == "127.0.0.1"
            assert pkt[1].ip.dst == "127.0.0.1"
            assert pkt[1].tcp.srcport == 0
            assert pkt[1].tcp.dstport == 80
        except Exception, e:
            self._queue.put(e)

class RevHostsThread(SniffThread):
    def run(self):
        pkt = umpa.sniffing.sniff(2, device=self._device, filter=self._filter)
        try:
            assert pkt[0].ip.src == "67.205.14.183"
            assert pkt[0].ip.dst == "127.0.0.1"
            assert pkt[1].ip.src == "127.0.0.1"
            assert pkt[1].ip.dst == "67.205.14.183"
        except Exception, e:
            self._queue.put(e)

class ForwardThread(SniffThread):
    def run(self):
        pkt = umpa.sniffing.sniff(2, device=self._device, filter=self._filter)
        try:
            assert pkt[0].ip.src == "127.0.0.1"
            assert pkt[0].ip.dst == "67.205.14.183"
            assert pkt[1].ip.src == "127.0.0.1"
            assert pkt[1].ip.dst == "127.0.0.1"
        except Exception, e:
            self._queue.put(e)

class TestModels(object):
    pass

class TestReact(TestModels):
    def test_revports(self):
        # use queue to communicate between threads
        # py.test doesn't catch assertions from threads by itself
        queue = Queue.Queue()

        th = SendPacket(umpa.Packet(IP(), TCP(srcport=80, dstport=0)))
        th.start()
        
        th2 = RevPortsThread("host 127.0.0.1 and port 80", "lo", queue)
        th2.start()
        models.react(1, filter="host 127.0.0.1 and port 80", device="lo",
                    revports=True)
        th.join()
        th2.join()
        if not queue.empty():
            err = queue.get()
            raise AssertionError(err)
        queue.join()

    def test_revhosts(self):
        # use queue to communicate between threads
        # py.test doesn't catch assertions from threads by itself
        queue = Queue.Queue()

        th = SendPacket(umpa.Packet(IP(src="67.205.14.183", dst="127.0.0.1")))
        th.start()
        
        th2 = RevHostsThread("host 67.205.14.183", "any", queue)
        th2.start()
        models.react(1, filter="host 67.205.14.183", device="any", revhosts=True)
        th.join()
        th2.join()
        if not queue.empty():
            err = queue.get()
            raise AssertionError(err)
        queue.join()
        
    def test_forward(self):
        # use queue to communicate between threads
        # py.test doesn't catch assertions from threads by itself
        queue = Queue.Queue()

        th = SendPacket(umpa.Packet(IP(src="127.0.0.1", dst="67.205.14.183"), TCP(srcport=888)))
        th.start()
        
        th2 = ForwardThread("host 127.0.0.1 and port 888", "any", queue)
        th2.start()
        models.react(1, filter="host 67.205.14.183 and port 888", device="any",
                    forward="127.0.0.1")
        th.join()
        th2.join()
        if not queue.empty():
            err = queue.get()
            raise AssertionError(err)
        queue.join()

    def test_wrongargs(self):
        py.test.raises(UMPAException, "models.react(1, foo=True)")
        py.test.raises(UMPAException,
                "models.react(1, foo=True, revports=True)")
        py.test.raises(UMPAException,
                "models.react(1, foo=False, revhosts=True)")
        py.test.raises(UMPAException, "models.react(1, foo=True, bar=False)")
