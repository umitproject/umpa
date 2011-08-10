#!/usr/bin/env python
"""
ICMPV6 (Internet Control Message Protocol for IPV6) implementation.
"""

import struct

from umit.umpa.protocols import _consts
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _protocols
from umit.umpa.protocols import _layer4
from umit.umpa.protocols import _layer4_ipv6
import umit.umpa.utils.net as _net
import umit.umpa.utils.bits as _bits

__all__ = [ "ICMPV6", ]



class _HType(_fields.EnumField):
    """
    This field contains the ICMP message type.
    """

    bits = 8
    auto = False
    enumerable = {
        "DESTINATION_UNREACHABLE" : _consts.ICMPV6_TYPE_DEST_UNREACHABLE,
        "PACKET_TOO_BIG" : _consts.ICMPV6_TYPE_PACKET_BIG,
        "TIME_EXCEED" : _consts.ICMPV6_TYPE_TIME_EXCEED,
        "TYPE_PARAMETER" : _consts.ICMPV6_TYPE_PARAMETER,
        "100" : _consts.ICMPV6_TYPE_PRIVATE_EXP100,
        "101" : _consts.ICMPV6_TYPE_PRIVATE_EXP101,
        "127" : _consts.ICMPV6_TYPE_RESERVED127,
        "ECHO" : _consts.ICMPV6_TYPE_ECHO_REQUEST,
        "ECHO_REPLY" : _consts.ICMPV6_TYPE_ECHO_REPLY,
        "ROUTER_SOLICITATION" : _consts.ICMPV6_TYPE_ROUTER_SOLICITATION,
        "ROUTER_ADVERTISMENT" : _consts.ICMPV6_TYPE_ROUTER_ADVERTISMENT,
        "135" : _consts.ICMPV6_TYPE_NEIGHBOUR_SOLICITATION,
        "136" : _consts.ICMPV6_TYPE_NEIGHBOUR_ADVERTISMENT,
        "137" : _consts.ICMPV6_TYPE_REDIRECT_MESSAGE,
        "138" : _consts.ICMPV6_TYPE_ROUTER_RENUMBERING,
        "139" : _consts.ICMPV6_TYPE_ICMP_NODE_QUERY,
        "140" : _consts.ICMPV6_TYPE_ICMP_NODE_RESPONSE,
        "141" : _consts.ICMPV6_TYPE_INDSM,
        "142" : _consts.ICMPV6_TYPE_INDAM,
        "144" : _consts.ICMPV6_TYPE_HAAD_REQUEST,
        "145" : _consts.ICMPV6_TYPE_HAAD_REPLY,
        "146" : _consts.ICMPV6_TYPE_MPS,
        "147" : _consts.ICMPV6_TYPE_MPA,
        "148" : _consts.ICMPV6_TYPE_CPS,
        "149" : _consts.ICMPV6_TYPE_CPA,
        "151" : _consts.ICMPV6_TYPE_MRA,
        "152" : _consts.ICMPV6_TYPE_MRS,
        "153" : _consts.ICMPV6_TYPE_MRT,
        "200" : _consts.ICMPV6_TYPE_PRIVATE_EXP200,
        "201" : _consts.ICMPV6_TYPE_PRIVATE_EXP201,
        "255" : _consts.ICMPV6_TYPE_RESERVED255,
    }

class _HCode(_fields.EnumField):
    """
    """

    bits = 8
    auto = False
    enumerable = {
        "NO_ROUTE_DEST" : _consts.ICMPV6_CODE_NO_ROUTE_DEST,
        "COMM_DEST_ADMIN_PROHIBITED" : _consts.ICMPV6_CODE_COMM_DEST_ADMIN_PROHIBITED,
        "BEYOND_SCOPE_SRC_ADD" : _consts.ICMPV6_CODE_BEYOND_SCOPE_SRC_ADD,
        "ADD_UNREACHABLE" : _consts.ICMPV6_CODE_ADD_UNREACHABLE,
        "PORT_UNREACHABLE" : _consts.ICMPV6_CODE_PORT_UNREACHABLE,
        "SRC_ADD_FAIL_POLICY" : _consts.ICMPV6_CODE_SRC_ADD_FAIL_POLICY,
        "REJECT_ROUTE_TO_DEST" : _consts.ICMPV6_CODE_REJECT_ROUTE_TO_DEST,
        "ERROR_SRC_ROUTING_HEADER" : _consts.ICMPV6_CODE_ERROR_SRC_ROUTING_HEADER,
        "NO_CODE" : _consts.ICMPV6_CODE_NO_CODE,
        "HOP_LIMIT_EXCEED" : _consts.ICMPV6_CODE_HOP_LIMIT_EXCEED,
        "FRAGMENT_REASSEMBLY_TIME_EXCEED" : _consts.ICMPV6_CODE_FRAGMENT_REASSEMBLY_TIME_EXCEED,
        "ERROR_HEADER_FIELD" : _consts.ICMPV6_CODE_ERROR_HEADER_FIELD,
        "UNRECOGINIZED_NEXT_HEADER" : _consts.ICMPV6_CODE_UNRECOGINIZED_NEXT_HEADER,
        "UNRECOGINIZED_IPV6_OPTION" : _consts.ICMPV6_CODE_UNRECOGINIZED_IPV6_OPTION,
        "ROUTER_RENUMBERING_COMMAND" : _consts.ICMPV6_CODE_ROUTER_RENUMBERING_COMMAND,
        "ROUTER_RENUMBERING_RESULT" : _consts.ICMPV6_CODE_ROUTER_RENUMBERING_RESULT,
        "SEQUENCE_NUMBER_RESET" : _consts.ICMPV6_CODE_SEQUENCE_NUMBER_RESET,
        "IPV6_QUERY" : _consts.ICMPV6_CODE_IPV6_QUERY,
        "NAME_QUERY" : _consts.ICMPV6_CODE_NAME_QUERY,
        "IPV4_QUERY" : _consts.ICMPV6_CODE_IPV4_QUERY,
        "SUCCESSFUL_REPLY" : _consts.ICMPV6_CODE_SUCCESSFUL_REPLY,
        "REFUSE_ANSWER" : _consts.ICMPV6_CODE_REFUSE_ANSWER,
        "QUERY_UNKNOWN" : _consts.ICMPV6_CODE_QUERY_UNKNOWN,
    }

class _HIdent(_fields.IntField):
    """
    """

    bits = 16

class _HSeq(_fields.IntField):
    """
    """

    bits = 16
    
class _HMtu(_fields.IntField):
    """
    """

    bits = 32

class _HPointer(_fields.IntField):
    """
    """

    bits = 32

    
class _HUnused(_fields.IntField):
    """
    """

    bits = 32
            
class ICMPV6(_protocols.Protocol):
    """
    """

    layer = 4
    protocol_id = _consts.NXT_ICMP
    payload_fieldname = None
    name = "ICMPV6"

    _ordered_fields = (# fixed header
                       'type', 'code', '_checksum',
                       # variable headers, one per line
                       'ident', 'seq',
                       'mtu',
                       'pointer',
                       'unused',
                       # data part, one per line
                       'data',
                       )
    def __init__(self, **kwargs):
        """
        """

        fields_list = [ ### Fixed header part:
                        _HType("Type"),
                        _HCode("Code", 0),
                        _layer4_ipv6.Layer4ChecksumField("Checksum"),
                        ### Variable header part:
                        _HIdent("Identifier", 0, active=False),
                        _HSeq("Sequence Number", 0, active=False),
                        _HMtu("Max Trans Unit", 64, active=False),
                        _HPointer("Pointer",0, active=False),
                        _HUnused("Unused", 0),
                        
                        ### Data part:
                        _fields.DataField("Data", ''),
                        ]

        super(ICMPV6, self).__init__(fields_list, **kwargs)


        self.get_field('_checksum').set_doc("Checksum of ICMP packet. "
            "See RFC 2443 for more info.")
            
    def __setattr__(self, attr, value):        
        """
        """
        super(ICMPV6, self).__setattr__(attr, value)   
        
        if attr == 'type':
            self.disable_fields('unused', 'ident', 'seq','pointer','mtu','data')
            # activate dynamic header fields depending on the type  
            if self.type in ( _consts.ICMPV6_TYPE_ECHO_REQUEST, _consts.ICMPV6_TYPE_ECHO_REPLY, ):
                self.enable_fields('ident', 'seq')
            elif self.type in (_consts.ICMPV6_TYPE_PARAMETER, ):
                self.enable_fields('pointer')
            elif self.type in (_consts.ICMPV6_TYPE_PACKET_BIG, ):
                self.enable_fields('mtu') 
            else:
                self.enable_fields('unused') 
            # activate data fields depending on the type
            self.enable_fields('data')
            
    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        """

        # Length
        self.get_field('_checksum')._tmp_value = protocol_bits

        return raw_value, bit            


    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        """
        
        # Fill checksum only if it's zero (not supplied by user)
        cksum_offset = bit - self.get_offset('_checksum') - \
                       self.get_field('_checksum').bits

        #self.get_field('_checksum')._tmp_value  = 32699
        if _bits.get_bits(raw_value,self.get_field('_checksum').bits,cksum_offset,rev_offset=True) == 0:

            # Payload
            if self.payload:
                cksum = self.payload.__dict__['__raw_value']
            else:
                cksum = 0
            offset = protocol_bits

            # TCP Header
            cksum |= raw_value << offset
            offset += bit
            
            
            # calculate checksum and place it at the correct offset in raw_value
            total_length = offset
            total_length /= 8
            pheader = _layer4_ipv6.PseudoHeader6(self.protocol_id, total_length)
            pheader_raw = pheader.get_raw(protocol_container, protocol_bits)[0]
            cksum |= pheader_raw << offset
            raw_cksum = _net.in_cksum(cksum)
            cksum_cal = ((raw_cksum << 8) | (raw_cksum >> 8)) & 0xFFFF
            raw_value |= cksum_cal << cksum_offset
            #cksum = _net.in_cksum(raw_value)
            #raw_value |= cksum << cksum_offset
            #self.get_field('_checksum')._tmp_value  = 32699

        return raw_value, bit

    def load_raw(self, buffer):
        """
        """

        header_size = 8
        header_format = '!BBHI'
        fields = struct.unpack(header_format, buffer[:header_size])
        buffer = buffer[header_size:]

        self.type = fields[0]
        self.code = fields[1]
        self._checksum = fields[2]

        # fill in dynamic header fields depending on the type
        if self.type in (_consts.ICMPV6_TYPE_ECHO_REQUEST, _consts.ICMPV6_TYPE_ECHO_REPLY,):
            self.ident = fields[3] >> 16
            self.seq   = fields[3] & 0x0000FFFF 
        else:
            self.unused = fields[3]

        # fill in data fields depending on the type
        self.data = buffer

        return buffer

protocols = [ ICMPV6, ]                   
