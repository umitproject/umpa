#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
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

"""
XML features

Packets can be loaded/saved from/to XML files.

2 functions are provided:
 1. save()
 2. load()

Also, Packet objects get 2 extra methods:
 1. Packet.save_xml()
 2. Packet.load_xml()
"""

import re
import xml.dom.minidom

import umit.umpa
from umit.umpa.protocols._fields import Flags

# TODO: refactoring with SAX usage

def save(filename, packets):
    """
    Save the list of Packet's objects into XML file.

    @type filename: C{str}
    @param filename: name of the XML file.

    @type packets: C{list}
    @param packets: list of packets which will be saved.
    """

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
                if isinstance(proto.get_field(field), Flags):
                    f.setAttribute("type", "bits")
                    for flag in proto.get_field(field)._ordered_fields:
                        b = doc.createElement(flag)
                        f.appendChild(b)
                        value = proto.get_field(field).get(flag)[0]
                        b.appendChild(doc.createTextNode(str(value)))
                        b.setAttribute("type",
                            parse_str.match(str(type(value))).group(1))
                else:
                    f.appendChild(doc.createTextNode(
                        str(proto.get_field(field).get())))
                    f.setAttribute("type", parse_str.match(
                        str(type(proto.get_field(field).get()))).group(1))

    # check if filename is not already opened
    try:
        filename.write(doc.toprettyxml())
    except AttributeError:
        open(filename, "w").write(doc.toprettyxml())

def load(filename, proto_only=False):
    """
    Load Packet's objects from the XML file.

    Normally, return list of objects' packets but if proto_only is True,
    just return list of protocols from the first loaded packet.
    It's usefull if in some cases.
    I{Example}:

        >>> import umit.umpa
        >>> import umit.umpa.extensions.XML
        >>> packet = umit.umpa.Packet()
        >>> packet.load_xml('packets.xml') # proto_only by default in this case
    
    In this case, don't create new objects of Packet. Return list of protocols
    intead.

    @type filename: C{str}
    @param filename: name of the XML file.

    @type proto_only: C{bool}
    @param proto_only: if True, return list of protocols from the first loaded
    packet (default: I{False}).

    @rtype: C{list}
    @return: loaded Packet's objects or list of protocols from the first
    loaded packet (if proto_only is True).
    """

    doc = xml.dom.minidom.parse(filename)

    # useful if you have type in string and need to cast it
    typemap = dict(float=float, int=int, str=str, bool=bool)
    packets = []
    for pa in doc.getElementsByTagName("packet"):
        is_true = (pa.getAttribute("strict") != "False")
        packet = umit.umpa.Packet(strict=is_true)
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
                        protocol.get_field(field_name).set(value)
                    # Flags
                    else:
                        for bit in node.childNodes:
                            if bit.nodeType == node.ELEMENT_NODE:
                                bit_name = bit.localName
                                bit_value = bit.childNodes[0].nodeValue.strip()
                                is_true = (bit_value == "True")
                                if is_true:
                                    protocol.get_field(field_name).set(
                                                                    bit_name)
                                else:
                                    protocol.get_field(field_name).set(False,
                                                                    bit_name)
            packet.include(protocol)

        # we only load first packet in the file and return list of protocols..
        if proto_only:
            return packet.protos
        packets.append(packet)
    return packets

def _save_xml(self, filename):
    """
    Save the Packet's object into XML file.

    @type filename: C{str}
    @param filename: name of the XML file.
    """

    save(filename, [self, ])

def _load_xml(self, filename):
    """
    Load defined protocols from the XML file.

    Overwrite current list of the protocols in the Packet's object by
    loaded protocols.
    
    Internally, call umit.umpa.extensions.XML.load() function
    with proto_only=True attribute.
    @type filename: C{str}
    @param filename: name of the XML file.
    """

    self.protos = load(filename, proto_only=True)

umit.umpa.Packet.save_xml = _save_xml
umit.umpa.Packet.load_xml = _load_xml
