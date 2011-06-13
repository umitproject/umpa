#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009-2010 Adriano Monteiro Marques.
#
# Authors: Bartosz SKOWRON <getxsick at gmail dot com>
#          Kosma Moczek <kosma at kosma dot pl>
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
import py.test

from umit.umpa import Socket, SocketL2, Packet
import umit.umpa.sniffing
from umit.umpa.protocols import Ethernet, IP, TCP, UDP, Payload ,IPV6 , TCP6
from umit.umpa.utils.exceptions import UMPAException, UMPANotPermittedException
from tests.utils import SendPacket, SendPacketL2

class TestUMPASockets(object):
    def test_init(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.raises(UMPANotPermittedException, "Socket()")

    def test_sent_size(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-privileges are needed')

        p1 = Packet(IP(), TCP())
        p2 = Packet(IP(), TCP())

        s = Socket()
        size = s.send(p1, p2)
        assert size == [40, 40]

    def test_send_size_L2(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-privileges are needed')

        p1 = Packet(Ethernet(src='00:11:22:33:44:55', dst='00:11:22:33:44:55'),
                    IP(src="127.0.0.1", dst="127.0.0.1"),
                    TCP(srcport=1234, dstport=4321),
                    Payload('xyz'))
        p2 = Packet(Ethernet(src='00:11:22:33:44:55', dst='00:11:22:33:44:55'),
                    IP(src="127.0.0.1", dst="127.0.0.1"),
                    TCP(srcport=1234, dstport=4321),
                    Payload('xyz'))

        s = SocketL2(iface='lo')
        size = s.send(p1, p2)

        assert size == [57, 57]

    def test_send_sniff_tcp(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-privileges are needed')

        p = Packet(Ethernet(src='00:11:22:33:44:55', dst='00:11:22:33:44:55'),
                   IP(src="127.0.0.1", dst="127.0.0.1"),
                   UDP(srcport=1234, dstport=4321),
                   Payload('xyz'))

        th = SendPacketL2(p, iface='lo')
        th.start()
        result = umit.umpa.sniffing.sniff(1, device='lo', filter="src port 1234")
        th.join()

        assert len(result) == 1
        assert result[0].ethernet.src == '00:11:22:33:44:55'
        assert result[0].ip.src == '127.0.0.1'
        assert result[0].udp.srcport == 1234
        assert result[0].udp.dstport == 4321

    def test_send_sniff_tcp_L2(self):
        if os.name == 'posix' and os.geteuid() != 0:
            py.test.skip('root-privileges are needed')

        p = Packet(Ethernet(src='00:11:22:33:44:55', dst='00:11:22:33:44:55'),
                   IP(src="127.0.0.1", dst="127.0.0.1"),
                   TCP(srcport=1234, dstport=4321),
                   Payload('xyz'))

        th = SendPacketL2(p, iface='lo')
        th.start()
        result = umit.umpa.sniffing.sniff(1, device='lo', filter="src port 1234")
        th.join()

        assert len(result) == 1
        assert result[0].ethernet.src == '00:11:22:33:44:55'
        assert result[0].ip.src == '127.0.0.1'
        assert result[0].tcp.srcport == 1234
        assert result[0].tcp.dstport == 4321

    def test_ntohs_quirk(self):
        raw1 = "ABCDEFGH"
        raw2 = umit.umpa._sockets._ntohs_quirk(raw1)

        assert raw2 == "ABDCEFHG"
