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


import xml.dom.minidom

from umpa.protocols._fields import Flags

def write(filename, *packets):
    # no packets? 
    if not packets:
        return

    doc = xml.dom.minidom.Document()
    root = doc.createElementNS(None, 'UMPA')
    doc.appendChild(root)

    for i, packet in enumerate(packets):
        pa = doc.createElementNS(None, 'packet')
        pa.setAttributeNS(None, "id", str(i))
        root.appendChild(pa)
        for proto in packet.protos:
            pr = doc.createElementNS(None, 'protocol')
            pr.setAttributeNS(None, "type", proto.name)
            pa.appendChild(pr)

            for field in proto.get_fields_keys():
                f = doc.createElementNS(None, field)
                pr.appendChild(f)
                # if Flags...we need care about BitFlags objects
                if isinstance(proto._get_field(field), Flags):
                    for flag in proto._get_field(field).get():
                        b = doc.createElementNS(None, flag)
                        f.appendChild(b)
                        b.appendChild(doc.createTextNode(
                            str(proto._get_field(field)._value[flag].get())))
                else:
                    f.appendChild(doc.createTextNode(
                        str(proto._get_field(field).get())))
    print doc.toprettyxml()
    open(filename, "w").write(doc.toprettyxml())


