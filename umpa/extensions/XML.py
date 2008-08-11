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


import re
import xml.dom.minidom

import umpa
from umpa.protocols._fields import Flags

def save(filename, packets):
    # for parsing python-object strings like <.... 'xxxx'>
    parse_str = re.compile(r"^.*'([\w\.]+)'>$")

    doc = xml.dom.minidom.Document()
    root = doc.createElement('UMPA')
    doc.appendChild(root)
    for i, packet in enumerate(packets):
        pa = doc.createElement('packet')
        pa.setAttribute("id", str(i))
        pa.setAttribute("strict", str(packet.strict))
        root.appendChild(pa)

        for proto in packet.protos:
            pr = doc.createElement('protocol')
            classname = parse_str.match(str(proto.__class__)).group(1)
            pr.setAttribute("class", classname)
            pa.appendChild(pr)

            for field in proto.get_fields_keys():
                f = doc.createElement(field)
                pr.appendChild(f)
                # if Flags...we need care about BitFlags objects
                if isinstance(proto._get_field(field), Flags):
                    f.setAttribute("type", "bits")
                    for flag in proto._get_field(field).get():
                        b = doc.createElement(flag)
                        f.appendChild(b)
                        value = proto._get_field(field)._value[flag].get()
                        b.appendChild(doc.createTextNode(str(value)))
                        b.setAttribute("type",
                            parse_str.match(str(type(value))).group(1))
                else:
                    f.appendChild(doc.createTextNode(
                        str(proto._get_field(field).get())))
                    f.setAttribute("type", parse_str.match(
                        str(type(proto._get_field(field).get()))).group(1))
    #print doc.toprettyxml()
    open(filename, "w").write(doc.toprettyxml())

def load(filename, proto_only=False):
    doc = xml.dom.minidom.parse(filename)

    # useful if you have type in string and need to cast it
    typemap = dict(float=float, int=int, str=str, bool=bool)

    packets = []
    for pa in doc.getElementsByTagName("packet"):
        is_true = (pa.getAttribute("strict") != "False")
        packet = umpa.Packet(strict=is_true)
        for pr in pa.getElementsByTagName("protocol"):
            # dealing with class of protocol
            protocol_name = pr.getAttribute("class").split(".")
            # we need to import proper class
            mname = '.'.join(protocol_name[:-1])
            cname = protocol_name[-1]
            mod = __import__(mname, fromlist=[None])
            # and create an instance
            clss = getattr(mod, cname)
            protocol = clss()
            
            for node in pr.childNodes:
                # because of pretty-style of XML files
                # we need to check if nodes are necessary
                if node.nodeType == node.ELEMENT_NODE:
                    field_name = node.localName

                    # checking if not Flags
                    type_node = node.getAttribute("type")
                    if type_node != "bits":
                        value = node.childNodes[0].nodeValue.strip()
                        if type_node == "NoneType":
                            value = None
                        else:
                            value = typemap[type_node](value)
                        protocol._get_field(field_name).set(value)
                    # Flags
                    else:
                        for bits in node.childNodes:
                            if bits.nodeType == node.ELEMENT_NODE:
                                bit_value = bits.localName
                                is_true = (bit_value == "True")
                                if is_true:
                                    protocol._get_field(field_name).set(
                                                                    bit_value)
                                else:
                                    protocol._get_field(field_name).unset(
                                                                    bit_value)
            packet.include(protocol)

        # we load lonly first packet in the file and return list of protocols..
        if proto_only:
            return packet.protos
    packets.append(packet)
    return packets

def save_xml(self, filename):
    save(filename, [self,])

def load_xml(self, filename):
    self.protos = load(filename, proto_only=True)

umpa.Packet.save_xml = save_xml
umpa.Packet.load_xml = load_xml
