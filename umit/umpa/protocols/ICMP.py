#!/usr/bin/env python

import struct

from umit.umpa.protocols import _consts
from umit.umpa.protocols import _fields
from umit.umpa.protocols import _protocols
from umit.umpa.protocols import _layer4
import umit.umpa.utils.net as _net
import umit.umpa.utils.bits as _bits

__all__ = [ "ICMP", ]

class _HType(_fields.EnumField):
    """
    This field contains the ICMP message type.
    """

    bits = 8
    auto = False
    enumerable = {
        "ADDRESS_MASK_REPLY" : _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,
        "ADDRESS_MASK_REQUEST" : _consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
        "ALTERNATE_HOST_ADDRESS" : _consts.ICMP_TYPE_ALTERNATE_HOST_ADDRESS,
        "DATAGRAM_CONVERSION_ERROR" : _consts.ICMP_TYPE_DATAGRAM_CONVERSION_ERROR,
        "DESTINATION_UNREACHABLE" : _consts.ICMP_TYPE_DESTINATION_UNREACHABLE,
        "DOMAIN_NAME_REPLY" : _consts.ICMP_TYPE_DOMAIN_NAME_REPLY,
        "DOMAIN_NAME_REQUEST" : _consts.ICMP_TYPE_DOMAIN_NAME_REQUEST,
        "ECHO" : _consts.ICMP_TYPE_ECHO,
        "ECHO_REPLY" : _consts.ICMP_TYPE_ECHO_REPLY,
        "ICMP_MESSAGES_UTILIZED" : _consts.ICMP_TYPE_ICMP_MESSAGES_UTILIZED,
        "INFORMATION_REPLY" : _consts.ICMP_TYPE_INFORMATION_REPLY,
        "INFORMATION_REQUEST" : _consts.ICMP_TYPE_INFORMATION_REQUEST,
        "IPV6_I_AM_HERE" : _consts.ICMP_TYPE_IPV6_I_AM_HERE,
        "IPV6_WHERE_ARE_YOU" : _consts.ICMP_TYPE_IPV6_WHERE_ARE_YOU,
        "MOBILE_HOST_REDIRECT" : _consts.ICMP_TYPE_MOBILE_HOST_REDIRECT,
        "MOBILE_REGISTRATION_REPLY" : _consts.ICMP_TYPE_MOBILE_REGISTRATION_REPLY,
        "MOBILE_REGISTRATION_REQUEST" : _consts.ICMP_TYPE_MOBILE_REGISTRATION_REQUEST,
        "PARAMETER_PROBLEM" : _consts.ICMP_TYPE_PARAMETER_PROBLEM,
        "PHOTURIS" : _consts.ICMP_TYPE_PHOTURIS,
        "REDIRECT" : _consts.ICMP_TYPE_REDIRECT,
        "RESERVED_ROBUSTNESS" : _consts.ICMP_TYPE_RESERVED_ROBUSTNESS,
        "RESERVED_SECURITY" : _consts.ICMP_TYPE_RESERVED_SECURITY,
        "ROUTER_ADVERTISEMENT" : _consts.ICMP_TYPE_ROUTER_ADVERTISEMENT,
        "ROUTER_SOLICITATION" : _consts.ICMP_TYPE_ROUTER_SOLICITATION,
        "SKIP" : _consts.ICMP_TYPE_SKIP,
        "SOURCE_QUENCH" : _consts.ICMP_TYPE_SOURCE_QUENCH,
        "TIME_EXCEEDED" : _consts.ICMP_TYPE_TIME_EXCEEDED,
        "TIMESTAMP" : _consts.ICMP_TYPE_TIMESTAMP,
        "TIMESTAMP_REPLY" : _consts.ICMP_TYPE_TIMESTAMP_REPLY,
        "TRACEROUTE" : _consts.ICMP_TYPE_TRACEROUTE,
        "1" : _consts.ICMP_TYPE_UNASSIGNED1,
        "2" : _consts.ICMP_TYPE_UNASSIGNED2,
        "7" : _consts.ICMP_TYPE_UNASSIGNED7,
        "42" : _consts.ICMP_TYPE_RESERVED42,
        "43" : _consts.ICMP_TYPE_RESERVED43,
        "44" : _consts.ICMP_TYPE_RESERVED44,
        "45" : _consts.ICMP_TYPE_RESERVED45,
        "46" : _consts.ICMP_TYPE_RESERVED46,
        "47" : _consts.ICMP_TYPE_RESERVED47,
        "48" : _consts.ICMP_TYPE_RESERVED48,
        "49" : _consts.ICMP_TYPE_RESERVED49,
        "50" : _consts.ICMP_TYPE_RESERVED50,
        "51" : _consts.ICMP_TYPE_RESERVED51,
        "52" : _consts.ICMP_TYPE_RESERVED52,
        "53" : _consts.ICMP_TYPE_RESERVED53,
        "54" : _consts.ICMP_TYPE_RESERVED54,
        "55" : _consts.ICMP_TYPE_RESERVED55,
        "56" : _consts.ICMP_TYPE_RESERVED56,
        "57" : _consts.ICMP_TYPE_RESERVED57,
        "58" : _consts.ICMP_TYPE_RESERVED58,
        "59" : _consts.ICMP_TYPE_RESERVED59,
        "60" : _consts.ICMP_TYPE_RESERVED60,
        "61" : _consts.ICMP_TYPE_RESERVED61,
        "62" : _consts.ICMP_TYPE_RESERVED62,
        "63" : _consts.ICMP_TYPE_RESERVED63,
        "64" : _consts.ICMP_TYPE_RESERVED64,
        "65" : _consts.ICMP_TYPE_RESERVED65,
        "66" : _consts.ICMP_TYPE_RESERVED66,
        "67" : _consts.ICMP_TYPE_RESERVED67,
        "68" : _consts.ICMP_TYPE_RESERVED68,
        "69" : _consts.ICMP_TYPE_RESERVED69,
        "70" : _consts.ICMP_TYPE_RESERVED70,
        "71" : _consts.ICMP_TYPE_RESERVED71,
        "72" : _consts.ICMP_TYPE_RESERVED72,
        "73" : _consts.ICMP_TYPE_RESERVED73,
        "74" : _consts.ICMP_TYPE_RESERVED74,
        "75" : _consts.ICMP_TYPE_RESERVED75,
        "76" : _consts.ICMP_TYPE_RESERVED76,
        "77" : _consts.ICMP_TYPE_RESERVED77,
        "78" : _consts.ICMP_TYPE_RESERVED78,
        "79" : _consts.ICMP_TYPE_RESERVED79,
        "80" : _consts.ICMP_TYPE_RESERVED80,
        "81" : _consts.ICMP_TYPE_RESERVED81,
        "82" : _consts.ICMP_TYPE_RESERVED82,
        "83" : _consts.ICMP_TYPE_RESERVED83,
        "84" : _consts.ICMP_TYPE_RESERVED84,
        "85" : _consts.ICMP_TYPE_RESERVED85,
        "86" : _consts.ICMP_TYPE_RESERVED86,
        "87" : _consts.ICMP_TYPE_RESERVED87,
        "88" : _consts.ICMP_TYPE_RESERVED88,
        "89" : _consts.ICMP_TYPE_RESERVED89,
        "90" : _consts.ICMP_TYPE_RESERVED90,
        "91" : _consts.ICMP_TYPE_RESERVED91,
        "92" : _consts.ICMP_TYPE_RESERVED92,
        "93" : _consts.ICMP_TYPE_RESERVED93,
        "94" : _consts.ICMP_TYPE_RESERVED94,
        "95" : _consts.ICMP_TYPE_RESERVED95,
        "96" : _consts.ICMP_TYPE_RESERVED96,
        "97" : _consts.ICMP_TYPE_RESERVED97,
        "98" : _consts.ICMP_TYPE_RESERVED98,
        "99" : _consts.ICMP_TYPE_RESERVED99,
        "100" : _consts.ICMP_TYPE_RESERVED100,
        "101" : _consts.ICMP_TYPE_RESERVED101,
        "102" : _consts.ICMP_TYPE_RESERVED102,
        "103" : _consts.ICMP_TYPE_RESERVED103,
        "104" : _consts.ICMP_TYPE_RESERVED104,
        "105" : _consts.ICMP_TYPE_RESERVED105,
        "106" : _consts.ICMP_TYPE_RESERVED106,
        "107" : _consts.ICMP_TYPE_RESERVED107,
        "108" : _consts.ICMP_TYPE_RESERVED108,
        "109" : _consts.ICMP_TYPE_RESERVED109,
        "110" : _consts.ICMP_TYPE_RESERVED110,
        "111" : _consts.ICMP_TYPE_RESERVED111,
        "112" : _consts.ICMP_TYPE_RESERVED112,
        "113" : _consts.ICMP_TYPE_RESERVED113,
        "114" : _consts.ICMP_TYPE_RESERVED114,
        "115" : _consts.ICMP_TYPE_RESERVED115,
        "116" : _consts.ICMP_TYPE_RESERVED116,
        "117" : _consts.ICMP_TYPE_RESERVED117,
        "118" : _consts.ICMP_TYPE_RESERVED118,
        "119" : _consts.ICMP_TYPE_RESERVED119,
        "120" : _consts.ICMP_TYPE_RESERVED120,
        "121" : _consts.ICMP_TYPE_RESERVED121,
        "122" : _consts.ICMP_TYPE_RESERVED122,
        "123" : _consts.ICMP_TYPE_RESERVED123,
        "124" : _consts.ICMP_TYPE_RESERVED124,
        "125" : _consts.ICMP_TYPE_RESERVED125,
        "126" : _consts.ICMP_TYPE_RESERVED126,
        "127" : _consts.ICMP_TYPE_RESERVED127,
        "128" : _consts.ICMP_TYPE_RESERVED128,
        "129" : _consts.ICMP_TYPE_RESERVED129,
        "130" : _consts.ICMP_TYPE_RESERVED130,
        "131" : _consts.ICMP_TYPE_RESERVED131,
        "132" : _consts.ICMP_TYPE_RESERVED132,
        "133" : _consts.ICMP_TYPE_RESERVED133,
        "134" : _consts.ICMP_TYPE_RESERVED134,
        "135" : _consts.ICMP_TYPE_RESERVED135,
        "136" : _consts.ICMP_TYPE_RESERVED136,
        "137" : _consts.ICMP_TYPE_RESERVED137,
        "138" : _consts.ICMP_TYPE_RESERVED138,
        "139" : _consts.ICMP_TYPE_RESERVED139,
        "140" : _consts.ICMP_TYPE_RESERVED140,
        "141" : _consts.ICMP_TYPE_RESERVED141,
        "142" : _consts.ICMP_TYPE_RESERVED142,
        "143" : _consts.ICMP_TYPE_RESERVED143,
        "144" : _consts.ICMP_TYPE_RESERVED144,
        "145" : _consts.ICMP_TYPE_RESERVED145,
        "146" : _consts.ICMP_TYPE_RESERVED146,
        "147" : _consts.ICMP_TYPE_RESERVED147,
        "148" : _consts.ICMP_TYPE_RESERVED148,
        "149" : _consts.ICMP_TYPE_RESERVED149,
        "150" : _consts.ICMP_TYPE_RESERVED150,
        "151" : _consts.ICMP_TYPE_RESERVED151,
        "152" : _consts.ICMP_TYPE_RESERVED152,
        "153" : _consts.ICMP_TYPE_RESERVED153,
        "154" : _consts.ICMP_TYPE_RESERVED154,
        "155" : _consts.ICMP_TYPE_RESERVED155,
        "156" : _consts.ICMP_TYPE_RESERVED156,
        "157" : _consts.ICMP_TYPE_RESERVED157,
        "158" : _consts.ICMP_TYPE_RESERVED158,
        "159" : _consts.ICMP_TYPE_RESERVED159,
        "160" : _consts.ICMP_TYPE_RESERVED160,
        "161" : _consts.ICMP_TYPE_RESERVED161,
        "162" : _consts.ICMP_TYPE_RESERVED162,
        "163" : _consts.ICMP_TYPE_RESERVED163,
        "164" : _consts.ICMP_TYPE_RESERVED164,
        "165" : _consts.ICMP_TYPE_RESERVED165,
        "166" : _consts.ICMP_TYPE_RESERVED166,
        "167" : _consts.ICMP_TYPE_RESERVED167,
        "168" : _consts.ICMP_TYPE_RESERVED168,
        "169" : _consts.ICMP_TYPE_RESERVED169,
        "170" : _consts.ICMP_TYPE_RESERVED170,
        "171" : _consts.ICMP_TYPE_RESERVED171,
        "172" : _consts.ICMP_TYPE_RESERVED172,
        "173" : _consts.ICMP_TYPE_RESERVED173,
        "174" : _consts.ICMP_TYPE_RESERVED174,
        "175" : _consts.ICMP_TYPE_RESERVED175,
        "176" : _consts.ICMP_TYPE_RESERVED176,
        "177" : _consts.ICMP_TYPE_RESERVED177,
        "178" : _consts.ICMP_TYPE_RESERVED178,
        "179" : _consts.ICMP_TYPE_RESERVED179,
        "180" : _consts.ICMP_TYPE_RESERVED180,
        "181" : _consts.ICMP_TYPE_RESERVED181,
        "182" : _consts.ICMP_TYPE_RESERVED182,
        "183" : _consts.ICMP_TYPE_RESERVED183,
        "184" : _consts.ICMP_TYPE_RESERVED184,
        "185" : _consts.ICMP_TYPE_RESERVED185,
        "186" : _consts.ICMP_TYPE_RESERVED186,
        "187" : _consts.ICMP_TYPE_RESERVED187,
        "188" : _consts.ICMP_TYPE_RESERVED188,
        "189" : _consts.ICMP_TYPE_RESERVED189,
        "190" : _consts.ICMP_TYPE_RESERVED190,
        "191" : _consts.ICMP_TYPE_RESERVED191,
        "192" : _consts.ICMP_TYPE_RESERVED192,
        "193" : _consts.ICMP_TYPE_RESERVED193,
        "194" : _consts.ICMP_TYPE_RESERVED194,
        "195" : _consts.ICMP_TYPE_RESERVED195,
        "196" : _consts.ICMP_TYPE_RESERVED196,
        "197" : _consts.ICMP_TYPE_RESERVED197,
        "198" : _consts.ICMP_TYPE_RESERVED198,
        "199" : _consts.ICMP_TYPE_RESERVED199,
        "200" : _consts.ICMP_TYPE_RESERVED200,
        "201" : _consts.ICMP_TYPE_RESERVED201,
        "202" : _consts.ICMP_TYPE_RESERVED202,
        "203" : _consts.ICMP_TYPE_RESERVED203,
        "204" : _consts.ICMP_TYPE_RESERVED204,
        "205" : _consts.ICMP_TYPE_RESERVED205,
        "206" : _consts.ICMP_TYPE_RESERVED206,
        "207" : _consts.ICMP_TYPE_RESERVED207,
        "208" : _consts.ICMP_TYPE_RESERVED208,
        "209" : _consts.ICMP_TYPE_RESERVED209,
        "210" : _consts.ICMP_TYPE_RESERVED210,
        "211" : _consts.ICMP_TYPE_RESERVED211,
        "212" : _consts.ICMP_TYPE_RESERVED212,
        "213" : _consts.ICMP_TYPE_RESERVED213,
        "214" : _consts.ICMP_TYPE_RESERVED214,
        "215" : _consts.ICMP_TYPE_RESERVED215,
        "216" : _consts.ICMP_TYPE_RESERVED216,
        "217" : _consts.ICMP_TYPE_RESERVED217,
        "218" : _consts.ICMP_TYPE_RESERVED218,
        "219" : _consts.ICMP_TYPE_RESERVED219,
        "220" : _consts.ICMP_TYPE_RESERVED220,
        "221" : _consts.ICMP_TYPE_RESERVED221,
        "222" : _consts.ICMP_TYPE_RESERVED222,
        "223" : _consts.ICMP_TYPE_RESERVED223,
        "224" : _consts.ICMP_TYPE_RESERVED224,
        "225" : _consts.ICMP_TYPE_RESERVED225,
        "226" : _consts.ICMP_TYPE_RESERVED226,
        "227" : _consts.ICMP_TYPE_RESERVED227,
        "228" : _consts.ICMP_TYPE_RESERVED228,
        "229" : _consts.ICMP_TYPE_RESERVED229,
        "230" : _consts.ICMP_TYPE_RESERVED230,
        "231" : _consts.ICMP_TYPE_RESERVED231,
        "232" : _consts.ICMP_TYPE_RESERVED232,
        "233" : _consts.ICMP_TYPE_RESERVED233,
        "234" : _consts.ICMP_TYPE_RESERVED234,
        "235" : _consts.ICMP_TYPE_RESERVED235,
        "236" : _consts.ICMP_TYPE_RESERVED236,
        "237" : _consts.ICMP_TYPE_RESERVED237,
        "238" : _consts.ICMP_TYPE_RESERVED238,
        "239" : _consts.ICMP_TYPE_RESERVED239,
        "240" : _consts.ICMP_TYPE_RESERVED240,
        "241" : _consts.ICMP_TYPE_RESERVED241,
        "242" : _consts.ICMP_TYPE_RESERVED242,
        "243" : _consts.ICMP_TYPE_RESERVED243,
        "244" : _consts.ICMP_TYPE_RESERVED244,
        "245" : _consts.ICMP_TYPE_RESERVED245,
        "246" : _consts.ICMP_TYPE_RESERVED246,
        "247" : _consts.ICMP_TYPE_RESERVED247,
        "248" : _consts.ICMP_TYPE_RESERVED248,
        "249" : _consts.ICMP_TYPE_RESERVED249,
        "250" : _consts.ICMP_TYPE_RESERVED250,
        "251" : _consts.ICMP_TYPE_RESERVED251,
        "252" : _consts.ICMP_TYPE_RESERVED252,
        "253" : _consts.ICMP_TYPE_RESERVED253,
        "254" : _consts.ICMP_TYPE_RESERVED254,
        "255" : _consts.ICMP_TYPE_RESERVED255,
    }

class _HCode(_fields.EnumField):
    """
    """

    bits = 8
    auto = False
    enumerable = {
        "ALTERNATE_ADDRESS_FOR_HOST" : _consts.ICMP_CODE_ALTERNATE_ADDRESS_FOR_HOST,
        "AUTHENTICATION_FAILED" : _consts.ICMP_CODE_AUTHENTICATION_FAILED,
        "BAD_LENGTH" : _consts.ICMP_CODE_BAD_LENGTH,
        "BAD_SPI" : _consts.ICMP_CODE_BAD_SPI,
        "COMMUNICATION_ADMINISTRATIVELY_PROHIBITED" : _consts.ICMP_CODE_COMMUNICATION_ADMINISTRATIVELY_PROHIBITED,
        "COMMUNICATION_WITH_HOST_PROHIBITED" : _consts.ICMP_CODE_COMMUNICATION_WITH_HOST_PROHIBITED,
        "COMMUNICATION_WITH_NETWORK_PROHIBITED" : _consts.ICMP_CODE_COMMUNICATION_WITH_NETWORK_PROHIBITED,
        "DECOMPRESSION_FAILED" : _consts.ICMP_CODE_DECOMPRESSION_FAILED,
        "DECRYPTION_FAILED" : _consts.ICMP_CODE_DECRYPTION_FAILED,
        "DESTINATION_HOST_UNKNOWN" : _consts.ICMP_CODE_DESTINATION_HOST_UNKNOWN,
        "DESTINATION_NETWORK_HOST_FOR_TOS" : _consts.ICMP_CODE_DESTINATION_NETWORK_HOST_FOR_TOS,
        "DESTINATION_NETWORK_UNKNOWN" : _consts.ICMP_CODE_DESTINATION_NETWORK_UNKNOWN,
        "DESTINATION_NETWORK_UNREACHABLE_FOR_TOS" : _consts.ICMP_CODE_DESTINATION_NETWORK_UNREACHABLE_FOR_TOS,
        "DOES_NOT_ROUTE_COMMON_TRAFFIC" : _consts.ICMP_CODE_DOES_NOT_ROUTE_COMMON_TRAFFIC,
        "FRAGMENTATION_NEEDED" : _consts.ICMP_CODE_FRAGMENTATION_NEEDED,
        "FRAGMENT_REASSEMBLY_TIME_EXCEED" : _consts.ICMP_CODE_FRAGMENT_REASSEMBLY_TIME_EXCEED,
        "HOST_PRECEDENCE_VIOLATION" : _consts.ICMP_CODE_HOST_PRECEDENCE_VIOLATION,
        "HOST_UNREACHABLE" : _consts.ICMP_CODE_HOST_UNREACHABLE,
        "MISSING_A_REQUIRED_OPTION" : _consts.ICMP_CODE_MISSING_A_REQUIRED_OPTION,
        "NEED_AUTHENTICATION" : _consts.ICMP_CODE_NEED_AUTHENTICATION,
        "NEED_AUTHORIZATION" : _consts.ICMP_CODE_NEED_AUTHORIZATION,
        "NET_UNREACHABLE" : _consts.ICMP_CODE_NET_UNREACHABLE,
        "NO_CODE" : _consts.ICMP_CODE_NO_CODE,
        "NORMAL_ROUTER_ADVERTISEMENT" : _consts.ICMP_CODE_NORMAL_ROUTER_ADVERTISEMENT,
        "POINTER_INDICATES_THE_ERROR" : _consts.ICMP_CODE_POINTER_INDICATES_THE_ERROR,
        "PORT_UNREACHABLE" : _consts.ICMP_CODE_PORT_UNREACHABLE,
        "PRECEDENCE_CUTOFF" : _consts.ICMP_CODE_PRECEDENCE_CUTOFF,
        "PROTOCOL_UNREACHABLE" : _consts.ICMP_CODE_PROTOCOL_UNREACHABLE,
        "REDIRECT_DATAGRAM_FOR_HOST" : _consts.ICMP_CODE_REDIRECT_DATAGRAM_FOR_HOST,
        "REDIRECT_DATAGRAM_FOR_NETWORK" : _consts.ICMP_CODE_REDIRECT_DATAGRAM_FOR_NETWORK,
        "REDIRECT_DATAGRAM_FOR_TOS_AND_HOST" : _consts.ICMP_CODE_REDIRECT_DATAGRAM_FOR_TOS_AND_HOST,
        "REDIRECT_DATAGRAM_FOR_TOS_AND_NETWORK" : _consts.ICMP_CODE_REDIRECT_DATAGRAM_FOR_TOS_AND_NETWORK,
        "SOURCE_HOST_ISOLATED" : _consts.ICMP_CODE_SOURCE_HOST_ISOLATED,
        "SOURCE_ROUTE_FAILED" : _consts.ICMP_CODE_SOURCE_ROUTE_FAILED,
        "TTL_EXCEED_IN_TRANSIT" : _consts.ICMP_CODE_TTL_EXCEED_IN_TRANSIT,
    }

class _HIdent(_fields.IntField):
    """
    """

    bits = 16

class _HSeq(_fields.IntField):
    """
    """

    bits = 16

class _HPointer(_fields.IntField):
    """
    """

    bits = 8

class _HPointerUnused(_fields.IntField):
    """
    """

    bits = 24

class _HUnused(_fields.IntField):
    """
    """

    bits = 32

class _HTimestamp(_fields.IntField):
    """
    """

    bits = 32

class ICMP(_protocols.Protocol):
    """
    ICMP (Internet Control Message Protocol) implementation.
    """

    layer = 4
    protocol_id = _consts.PROTOCOL_ICMP
    payload_fieldname = None
    name = "ICMP"


    _ordered_fields = (# fixed header
                       'type', 'code', '_checksum',
                       # variable headers, one per line
                       'ident', 'seq',
                       'redir_gw',
                       'pointer', 'pointer_unused',
                       'unused',
                       # data part, one per line
                       'originate', 'receive', 'transmit',
                       'addressmask',
                       'data',
                       )

    def __init__(self, **kwargs):
        """
        Create a new ICMP().
        """

        fields_list = [ ### Fixed header part:
                        _HType("Type"),
                        _HCode("Code", 0),
                        _layer4.Layer4ChecksumField("Checksum"),
                        ### Variable header part:
                        _HIdent("Identifier", 0, active=False),
                        _HSeq("Sequence Number", 0, active=False),
                        _fields.IPv4AddrField("Gateway Internet Address",
                                              '0.0.0.0', active=False),
                        _HPointer("Pointer", active=False),
                        _HPointerUnused("Unused", 0, active=False),
                        _HUnused("Unused", 0),
                        ### Data part:
                        _HTimestamp("Originate Timestamp", 0, active=False),
                        _HTimestamp("Receive Timestamp", 0, active=False),
                        _HTimestamp("Transmit Timestamp", 0, active=False),
                        _fields.IPv4AddrField("Address Mask",
                                              '0.0.0.0', active=False),
                        _fields.DataField("Data", ''),
                        ]

        # we call super.__init__ after prepared necessary data
        super(ICMP, self).__init__(fields_list, **kwargs)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self.get_field('_checksum').set_doc("Checksum of ICMP packet. "
            "See RFC 792 for more info.")
        self.get_field('redir_gw').set_doc("ICMP Redirect destination. "
            "See RFC 792 for more info.")
        self.get_field('addressmask').set_doc("Address Mask."
            "See RFC 950 for more info.")

    def __setattr__(self, attr, value):
        """
        """

        super(ICMP, self).__setattr__(attr, value)


        if attr == 'type':
            # disable all variable fields initially
            self.disable_fields('unused', 'ident', 'seq', 'redir_gw', 'pointer','pointer_unused','originate', 'receive', 'transmit','addressmask', 'data')

            # activate dynamic header fields depending on the type
            if self.type in (_consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
                             _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,
                             _consts.ICMP_TYPE_ECHO,
                             _consts.ICMP_TYPE_ECHO_REPLY,
                             _consts.ICMP_TYPE_INFORMATION_REQUEST,
                             _consts.ICMP_TYPE_INFORMATION_REPLY,
                             _consts.ICMP_TYPE_TIMESTAMP,
                             _consts.ICMP_TYPE_TIMESTAMP_REPLY,):
                self.enable_fields('ident', 'seq')
            elif self.type in (_consts.ICMP_TYPE_REDIRECT, ):
                self.enable_fields('redir_gw')
            elif self.type in (_consts.ICMP_TYPE_PARAMETER_PROBLEM, ):
                self.enable_fields('pointer', 'pointer_unused')
            else:
                # insert a dummy 4-byte field by default
                self.enable_fields('unused')

            # activate data fields depending on the type
            if self.type in (_consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
                             _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,):
                self.enable_fields('addressmask')
            elif self.type in (_consts.ICMP_TYPE_TIMESTAMP,
                               _consts.ICMP_TYPE_TIMESTAMP_REPLY,):
                self.enable_fields('originate', 'receive', 'transmit')
            else:
                # unknown/generic data
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
        print "proto bit "
        print protocol_bits

        # Fill checksum only if it's zero (not supplied by user)
        cksum_offset = bit - self.get_offset('_checksum') - \
                       self.get_field('_checksum').bits

        if _bits.get_bits(raw_value,self.get_field('_checksum').bits,cksum_offset,rev_offset=True) == 0:

            # calculate checksum and place it at the correct offset in raw_value
            cksum = _net.in_cksum(raw_value)
            raw_value |= cksum << cksum_offset

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
        if self.type in (_consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
                         _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,
                         _consts.ICMP_TYPE_ECHO,
                         _consts.ICMP_TYPE_ECHO_REPLY,
                         _consts.ICMP_TYPE_INFORMATION_REQUEST,
                         _consts.ICMP_TYPE_INFORMATION_REPLY,
                         _consts.ICMP_TYPE_TIMESTAMP,
                         _consts.ICMP_TYPE_TIMESTAMP_REPLY,):
            self.ident = fields[3] >> 16
            self.seq   = fields[3] & 0x0000FFFF
        elif self.type in (_consts.ICMP_TYPE_REDIRECT, ):
            
            addr = []
            addr.append((fields[3]>>24) & 0xff)
            addr.append((fields[3]>>16) & 0xff)
            addr.append((fields[3]>> 8) & 0xff)
            addr.append((fields[3]    ) & 0xff)
            self.redir_gw = '.'.join("%s" % addr_part for addr_part in addr)
        elif self.type in (_consts.ICMP_TYPE_PARAMETER_PROBLEM, ):
            self.pointer = fields[3] >> 24
            self.pointer_unused = fields[3] & 0x00ffffff
        else:
            self.unused = fields[3]

        # fill in data fields depending on the type
        if self.type in (_consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
                         _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,):
            data_size = 4
            data_format = "!4B"
            fields = struct.unpack(data_format, buffer[:data_size])
            buffer = buffer[data_size:]

            self.addressmask = '%d.%d.%d.%d' %  (fields[0:4] )
            
        elif self.type in (_consts.ICMP_TYPE_TIMESTAMP,
                           _consts.ICMP_TYPE_TIMESTAMP_REPLY,):
            data_size = 12
            data_format = "!3I"
            fields = struct.unpack(data_format, buffer[:data_size])
            buffer = buffer[data_size:]

            self.originate = fields[0]
            self.receive = fields[1]
            self.transmit = fields[2]
        else:
            # unknown/generic data
            self.data = buffer

        return buffer

protocols = [ ICMP, ]
