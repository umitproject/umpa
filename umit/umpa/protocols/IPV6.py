#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
#
# Author: Gaurav Ranjan <g.ranjan143@gmail.com>
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
IPv6 (Internet Protocol version 6 ) protocol implementation.
"""

import sys
import struct

from umit.umpa.protocols import _consts
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _protocols
import umit.umpa.utils.net as _net
import umit.umpa.utils.bits as _bits


class _HVersion(_fields.EnumField):
    """
    The Version field indicates the format of the internet header for Ipv6.
    
    """
    bits = 4
    auto = True

    def _generate_value(self):
        """
        """

        return _consts.IPVERSION_6
        
class _TClassDSCP(_fields.SpecialIntField):
    """
    This is a part of 8 bit Traffic class (divide into thrree part)
    DSCP , ECT , ECN-CE
    """
    bits = 6
    auto = True
    
    def _generate_value(self):
        """
        """
        
        return 0
class _FLabel(_fields.IntField):
    """
    Used for specifying special router handling from source to 
    destination(s) for a sequence of packets.
    """
    
    bits = 20
    auto = True

    def _generate_value(self):
        """
        """

        return 1
        
                
class  _PLoad(_fields.SpecialIntField):
	"""
	This field contation value of payload in Ipv6 header 
	"""
	bits = 16
	auto = True
	
	def _generate_value(self):
		"""
		
		
		"""
		return self._tmp_value / _consts.BYTE

		
		
class _NHeader(_fields.SpecialIntField, _fields.EnumField):
    """
    This field indicates the next level protocol used in the data portion
    of the internet datagram.
    
    """

    bits = 8
    auto = True
    enumerable = {
        "HBH"                      			: _consts.NXT_HBH ,
        "ICMP(Ipv4)"                        : _consts.NXT_ICMP,
        "IGMP"                				: _consts.NXT_IGMP,
        "GGP Gateway-to-Gateway Protocol"   : _consts.NXT_GGP,
        "IP"                                : _consts.NXT_IP,
        "ST"                               	: _consts.NXT_ST,
        "TCP"                               : _consts.NXT_TCP,
        "EGP"                            	: _consts.NXT_EGP,
        "IGP"                				: _consts.NXT_IGP,
        "CHAOS"                             : _consts.NXT_CHAOS,
        "UDP"                               : _consts.NXT_UDP,
        "ISOTP4"                          	: _consts.NXT_ISOTP4,
        "XTP"                           	: _consts.NXT_XTP,
        "RH"                              	: _consts.NXT_RH,
        "FH"                             	: _consts.NXT_FH,
        "IDRP"                              : _consts.NXT_IDRP,
        "RSVP"                      		: _consts.NXT_RSVP,
        "ESP"                               : _consts.NXT_ESP,
        "AH"                    			: _consts.NXT_AH,
        "NHRP"                 				: _consts.NXT_NHRP,
        "IPCM(Ipv6)"         				: _consts.NXT_ICMP,
        "Null"                				: _consts.NXT_Null,
        "DOH"                 				: _consts.NXT_DOH,
        "ISOIP"      						: _consts.NXT_ISOIP,
        "VINES"        						: _consts.NXT_VINES,
        "IGRP"               				: _consts.NXT_IGRP,
        "OSPF"                    			: _consts.NXT_OSPF,
        "AX_25"                    			: _consts.NXT_AX_25,
    }

    def _generate_value(self):
        """
        """

        return self._tmp_value

class  _HLimit(_fields.IntField):
	"""
	Hop limit tell about maximum hop a packet can travel before descrcaered default 255
	"""
	bits = 8
	auto = True
	
	def _generate_value(self):
		"""
		
		
		"""
		return 255



class IPV6(_protocols.Protocol):
	"""

	"""

	layer = 3      # layer of OSI
	protocol_id = _consts.ETHERTYPE_IPV6
	payload_fieldname = '_proto'
	name = "IPV6"

	_ordered_fields = ('_version','dscp','ds','_flow_label','_payload','_nxt_hdr','_hop_limit','src','dst',)


	def __init__(self, **kwargs):
		"""
		Create a new IPV6().
		"""

		tos = ('ect','ecn_ce')
		tos_predefined = dict.fromkeys(tos, 0)

		
		fields_list = [ _HVersion("Version",6),
					 _TClassDSCP("dscp", 0),
					 _fields.Flags("TOS", tos, **tos_predefined),
					 _FLabel("Flow label",0),
					 _PLoad("Pay Load"),
					 _NHeader("Next header"),
					 _HLimit("Hop Limit"),
					 _fields.IPv6AddrField("Source Address", "0:0:0:0:0:0:0:1"),
					 _fields.IPv6AddrField("Destination Address","0:0:0:0:0:0:0:1")]
		
		
		
		
		#
		super(IPV6, self).__init__(fields_list, **kwargs)

		# set __doc__ for fields - it's important if you want to get hints
		# in some frontends. E.g. Umit Project provides one...
		self.get_field('dscp').set_doc("This 6-bit field is similar in spirit to the ToS field in IPv4 but it is part 8 bit traffic class field")
		self.get_field('_flow_label').set_doc("Used for specifying special router handling from source to destination(s) for a sequence of packets.")
		self.get_field('_payload').set_doc("This 16-bit value is treated as an unsigned integer giving the number of bytes in the IPv6 datagram following 												the 40-byte packet header.")
		self.get_field('_nxt_hdr').set_doc("Specifies the next encapsulated protocol. The values are compatible with those specified for the IPv4 protocol 												field.")
		self.get_field('_hop_limit').set_doc("For each router that forwards the packet, the hop limit is decremented by 1. When the hop limit field 						      reaches zero, the packet is discarded. This replaces the TTL field in the IPv4 header that was originally 												intended to be used as a time based hop limit.")
		self.get_field('src').set_doc("The IPv6 address of the sending node.")
		self.get_field('dst').set_doc("The IPv6 address of the destination node.")

	def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
		"""
		"""

		self.get_field('_payload')._tmp_value = protocol_bits
		# Next Header protocol
		# field indicates the next level protocol used in the data
		# portion of the internet datagram.
		if self.payload:
		    proto_id = self.payload.protocol_id
		else:
		    proto_id = 6 
		self.get_field('_nxt_hdr')._tmp_value = proto_id

		return raw_value, bit

	def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
		"""
		Handle with fields after calling fillout() for them.

		"""

		return raw_value, bit

	def load_raw(self, buffer):
		"""
		"""

		header_size = 40
		header_format = '!IHBB8H8H'
		fields = struct.unpack(header_format, buffer[:header_size])

		self._version = fields[0] >> 28
		self._taffic_class = (fields[0] & 0x0FF00000) >> 8
		self._flow_label = fields[0] & 0x000FFFFF
		self._payload = fields[1]
		self._nxt_hdr = fields[2]
		self._hop_limit = fields[3]
		self.src = ':'.join(["%.4x"] * 8) % (fields[4:12])
		self.dst = ':'.join(["%.4x"] * 8) % (fields[4:12])

		# check if options are not missed
		

		return buffer[header_size:]

protocols = [ IPV6, ]
