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

import umit.umpa
import umit.umpa.protocols
from umit.umpa.protocols import Payload

def _prepare_protos():
    d = {2:[], 3:[], 4:[], 5:[]}
    for cls in umit.umpa.protocols.get_all().values():
        d[cls.layer].append(cls)
    return d

def decode(buffer, linktype):
    """
    Decode raw buffer of packet and return umit.umpa.Packet's object.
    
    @param buffer: raw buffer

    @type linktype: C{int}
    @param linktype: datalink of 2nd layer
    (return by datalink() method of pcap session)

    @rtype: C{umit.umpa.Packet}
    @return: decoded packet
    """

    protos = _prepare_protos()
    packet = umit.umpa.Packet(strict=False, warn=False)

    # XXX: currently there is no protocols in upper layers (above 4th layer)
    #      propably if they would be implemented - some changes are needed
    #      to detect what protocol it is
    #      statical version of decode was existing till r5043
    next_type = linktype
    layer = 2
    while next_type:
        for proto in protos[layer]:
            if next_type == proto.protocol_id:
                header = proto()
                buffer = header.load_raw(buffer)
                if header.payload_fieldname:
                    next_type = getattr(header, header.payload_fieldname)
                else:
                    next_type = None
                packet.include(header)
                break
        else:
            header = Payload()
            header.load_raw(buffer)
            packet.include(header)
            return packet
        layer += 1
    
    # payload
    if len(buffer) > 0:
        data = Payload()
        data.load_raw(buffer)
        packet.include(data)

    return packet
