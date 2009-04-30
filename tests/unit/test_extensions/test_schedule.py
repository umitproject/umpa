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

import os
import time

import py.test

import umpa
from umpa.protocols import IP
from umpa.extensions import schedule
from umpa.utils.exceptions import UMPAException


class TestExtensionSchedule(object):
    def test_send_schedule_attr(self):
        assert hasattr(umpa.Socket, 'send_schedule')

    def test_wrong_arg(self):
        py.test.raises(UMPAException, "schedule.send(0, bad_args=None)")
        py.test.raises(UMPAException,
                            "schedule.send(0, interval=10, bad_args=None)")

class TestExtensionScheduleRoot(object):
    def setup_class(cls):
        # EUID has to be 0 for POSIX
        if os.name == 'posix' and os.geteuid()!=0:
            py.test.skip('root-priviliges are needed')

    def test_extra_args(self):
        schedule.send(0, umpa.Packet(IP()))
        schedule.send(0, (umpa.Packet(IP()), umpa.Packet(IP())))
        schedule.send(0, [umpa.Packet(IP()), umpa.Packet(IP())])
        schedule.send(0, (umpa.Packet(IP()), umpa.Packet(IP())),
                                                            umpa.Packet(IP()))
        schedule.send(0, (umpa.Packet(IP()), umpa.Packet(IP())),
                                        umpa.Packet(IP()), umpa.Packet(IP()))

    def test_detach(self):
        try:
            schedule.send(0, [], detach=True)
        except NotImplementedError:
            py.test.skip("not implemented yet")

    def test_delay(self):
        delay = 2
        before = int(time.time())
        schedule.send(delay)
        after = int(time.time())
        assert after-before >= delay

    def test_interval(self):
        # TODO: should be test better when async will be available
        interval = 2
        p = (umpa.Packet(IP()), umpa.Packet(IP()))
        before = int(time.time())
        schedule.send(0, p, interval=interval)
        after = int(time.time())
        assert after-before >= interval*len(p)
