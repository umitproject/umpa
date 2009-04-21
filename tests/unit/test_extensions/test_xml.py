#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
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

from cStringIO import StringIO

import umpa
from umpa.protocols import IP, TCP, Payload
from umpa.protocols._fields import Flags
from umpa.extensions import XML

class TestExtensionXML(object):
    example_xml = """<?xml version="1.0" ?>
<UMPA>
        <packet id="0" strict="True">
                <protocol class="umpa.protocols.IP.IP">
                        <_version type="int">
                                4
                        </_version>
                        <_ihl type="NoneType">
                                None
                        </_ihl>
                        <type_of_service type="bits">
                                <relibility type="bool">
                                        False
                                </relibility>
                                <reserved0 type="bool">
                                        False
                                </reserved0>
                                <delay type="bool">
                                        False
                                </delay>
                                <throughput type="bool">
                                        False
                                </throughput>
                                <reserved1 type="bool">
                                        False
                                </reserved1>
                                <precedence2 type="bool">
                                        False
                                </precedence2>
                                <precedence1 type="bool">
                                        False
                                </precedence1>
                                <precedence0 type="bool">
                                        False
                                </precedence0>
                        </type_of_service>
                        <_total_length type="NoneType">
                                None
                        </_total_length>
                        <_identification type="int">
                                0
                        </_identification>
                        <flags type="bits">
                                <df type="bool">
                                        False
                                </df>
                                <mf type="bool">
                                        False
                                </mf>
                                <reserved type="bool">
                                        False
                                </reserved>
                        </flags>
                        <_fragment_offset type="int">
                                0
                        </_fragment_offset>
                        <time_to_live type="int">
                                64
                        </time_to_live>
                        <_protocol type="NoneType">
                                None
                        </_protocol>
                        <_header_checksum type="int">
                                0
                        </_header_checksum>
                        <source_address type="str">
                                127.0.0.1
                        </source_address>
                        <destination_address type="str">
                                67.205.14.183
                        </destination_address>
                        <options type="bits"/>
                        <_padding type="int">
                                0
                        </_padding>
                </protocol>
                <protocol class="umpa.protocols.TCP.TCP">
                        <source_port type="int">
                                2958
                        </source_port>
                        <destination_port type="int">
                                0
                        </destination_port>
                        <_sequence_number type="NoneType">
                                None
                        </_sequence_number>
                        <_acknowledgment_number type="NoneType">
                                None
                        </_acknowledgment_number>
                        <_data_offset type="NoneType">
                                None
                        </_data_offset>
                        <_reserved type="int">
                                0
                        </_reserved>
                        <control_bits type="bits">
                                <psh type="bool">
                                        False
                                </psh>
                                <urg type="bool">
                                        False
                                </urg>
                                <ack type="bool">
                                        False
                                </ack>
                                <syn type="bool">
                                        True
                                </syn>
                                <rst type="bool">
                                        False
                                </rst>
                                <fin type="bool">
                                        False
                                </fin>
                        </control_bits>
                        <_window type="NoneType">
                                None
                        </_window>
                        <_checksum type="NoneType">
                                None
                        </_checksum>
                        <_urgent_pointer type="NoneType">
                                None
                        </_urgent_pointer>
                        <options type="bits"/>
                        <_padding type="int">
                                0
                        </_padding>
                </protocol>
                <protocol class="umpa.protocols.Payload.Payload">
                        <data type="str">
                                this is umpa!
                        </data>
                </protocol>
        </packet>
</UMPA>
"""

    ip = IP()
    ip.source_address = "127.0.0.1"
    ip.destination_address = "67.205.14.183"

    # TCP header
    tcp = TCP()
    tcp.source_port = 2958
    tcp.destination_port = 0
    tcp.set_flags('control_bits', syn=True)

    # Payload
    data = Payload()
    data.data = "this is umpa!"

    # packet
    example_packet = umpa.Packet(ip, tcp, data)

    def test_packet_attrs(self):
        assert hasattr(umpa.Packet, 'save_xml')
        assert hasattr(umpa.Packet, 'load_xml')

    def test_xml_load(self):
        f = StringIO()
        f.write(self.example_xml)
        f.seek(0)

        packets = XML.load(f)

        for p in packets:
            for i, proto in enumerate(p.protos):
                for fieldname in proto.get_fields_keys():
                    assert proto.get_field(fieldname).fillout() == \
                self.example_packet.protos[i].get_field(fieldname).fillout()

    def test_xml_save(self):
        output = StringIO()
        XML.save(output, (self.example_packet,))
        a = output.getvalue()
        b = self.example_xml.replace('        ','\t')
        assert a == b
