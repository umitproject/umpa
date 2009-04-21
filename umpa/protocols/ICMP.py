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
ICMP (Internet Control Message Protocol) protocol implementation.
"""

from umpa.protocols import _consts
from umpa.protocols import _fields
from umpa.protocols import _protocols

__all__ = [ "ICMP", ]

class _HType(_fields.EnumField):
    bits = 8
    auto = False
    enumerable = {
        "Echo Reply"	: _consts.ICMP_TYPE_ECHO_REPLY,
        "Unassigned (1)"	: _consts.ICMP_TYPE_UNASSIGNED1,
        "Unassigned (2)"	: _consts.ICMP_TYPE_UNASSIGNED2,
        "Destination Unreachable"	:
                                    _consts.ICMP_TYPE_DESTINATION_UNREACHABLE,
        "Source Quench"	: _consts.ICMP_TYPE_SOURCE_QUENCH,
        "Redirect"	: _consts.ICMP_TYPE_REDIRECT,
        "Alternate Host Address"	: _consts.ICMP_TYPE_ALTERNATE_HOST_ADDRESS,
        "Unassigned (7)"	: _consts.ICMP_TYPE_UNASSIGNED7,
        "Echo"	: _consts.ICMP_TYPE_ECHO,
        "Router Advertisement"	: _consts.ICMP_TYPE_ROUTER_ADVERTISEMENT,
        "Router Solicitation"	: _consts.ICMP_TYPE_ROUTER_SOLICITATION,
        "Time Exceeded"	: _consts.ICMP_TYPE_TIME_EXCEEDED,
        "Parameter Problem"	: _consts.ICMP_TYPE_PARAMETER_PROBLEM,
        "Timestamp"	: _consts.ICMP_TYPE_TIMESTAMP,
        "Timestamp Reply"	: _consts.ICMP_TYPE_TIMESTAMP_REPLY,
        "Information Request"	: _consts.ICMP_TYPE_INFORMATION_REQUEST,
        "Information Reply"	: _consts.ICMP_TYPE_INFORMATION_REPLY,
        "Address Mask Request"	: _consts.ICMP_TYPE_ADDRESS_MASK_REQUEST,
        "Address Mask Reply"	: _consts.ICMP_TYPE_ADDRESS_MASK_REPLY,
        "Reserved Security"	: _consts.ICMP_TYPE_RESERVED_SECURITY,
        "Reserved Robustness"	: _consts.ICMP_TYPE_RESERVED_ROBUSTNESS,
        "Traceroute"	: _consts.ICMP_TYPE_TRACEROUTE,
        "Datagram Conversion Error"	:
                                _consts.ICMP_TYPE_DATAGRAM_CONVERSION_ERROR,
        "Mobile Host Redirect"	: _consts.ICMP_TYPE_MOBILE_HOST_REDIRECT,
        "Ipv (6) Where-Are-You"	: _consts.ICMP_TYPE_IPV6_WHERE_ARE_YOU,
        "Ipv (6) I-Am-Here"	: _consts.ICMP_TYPE_IPV6_I_AM_HERE,
        "Mobile Registration Request"	:
                                _consts.ICMP_TYPE_MOBILE_REGISTRATION_REQUEST,
        "Mobile Registration Reply"	:
                                _consts.ICMP_TYPE_MOBILE_REGISTRATION_REPLY,
        "Domain Name Request"	: _consts.ICMP_TYPE_DOMAIN_NAME_REQUEST,
        "Domain Name Reply"	: _consts.ICMP_TYPE_DOMAIN_NAME_REPLY,
        "Skip"	: _consts.ICMP_TYPE_SKIP,
        "Photuris"	: _consts.ICMP_TYPE_PHOTURIS,
        "Icmp Messages Utilized"	: _consts.ICMP_TYPE_ICMP_MESSAGES_UTILIZED,
        "Reserved (42)"	: _consts.ICMP_TYPE_RESERVED42,
        "Reserved (43)"	: _consts.ICMP_TYPE_RESERVED43,
        "Reserved (44)"	: _consts.ICMP_TYPE_RESERVED44,
        "Reserved (45)"	: _consts.ICMP_TYPE_RESERVED45,
        "Reserved (46)"	: _consts.ICMP_TYPE_RESERVED46,
        "Reserved (47)"	: _consts.ICMP_TYPE_RESERVED47,
        "Reserved (48)"	: _consts.ICMP_TYPE_RESERVED48,
        "Reserved (49)"	: _consts.ICMP_TYPE_RESERVED49,
        "Reserved (50)"	: _consts.ICMP_TYPE_RESERVED50,
        "Reserved (51)"	: _consts.ICMP_TYPE_RESERVED51,
        "Reserved (52)"	: _consts.ICMP_TYPE_RESERVED52,
        "Reserved (53)"	: _consts.ICMP_TYPE_RESERVED53,
        "Reserved (54)"	: _consts.ICMP_TYPE_RESERVED54,
        "Reserved (55)"	: _consts.ICMP_TYPE_RESERVED55,
        "Reserved (56)"	: _consts.ICMP_TYPE_RESERVED56,
        "Reserved (57)"	: _consts.ICMP_TYPE_RESERVED57,
        "Reserved (58)"	: _consts.ICMP_TYPE_RESERVED58,
        "Reserved (59)"	: _consts.ICMP_TYPE_RESERVED59,
        "Reserved (60)"	: _consts.ICMP_TYPE_RESERVED60,
        "Reserved (61)"	: _consts.ICMP_TYPE_RESERVED61,
        "Reserved (62)"	: _consts.ICMP_TYPE_RESERVED62,
        "Reserved (63)"	: _consts.ICMP_TYPE_RESERVED63,
        "Reserved (64)"	: _consts.ICMP_TYPE_RESERVED64,
        "Reserved (65)"	: _consts.ICMP_TYPE_RESERVED65,
        "Reserved (66)"	: _consts.ICMP_TYPE_RESERVED66,
        "Reserved (67)"	: _consts.ICMP_TYPE_RESERVED67,
        "Reserved (68)"	: _consts.ICMP_TYPE_RESERVED68,
        "Reserved (69)"	: _consts.ICMP_TYPE_RESERVED69,
        "Reserved (70)"	: _consts.ICMP_TYPE_RESERVED70,
        "Reserved (71)"	: _consts.ICMP_TYPE_RESERVED71,
        "Reserved (72)"	: _consts.ICMP_TYPE_RESERVED72,
        "Reserved (73)"	: _consts.ICMP_TYPE_RESERVED73,
        "Reserved (74)"	: _consts.ICMP_TYPE_RESERVED74,
        "Reserved (75)"	: _consts.ICMP_TYPE_RESERVED75,
        "Reserved (76)"	: _consts.ICMP_TYPE_RESERVED76,
        "Reserved (77)"	: _consts.ICMP_TYPE_RESERVED77,
        "Reserved (78)"	: _consts.ICMP_TYPE_RESERVED78,
        "Reserved (79)"	: _consts.ICMP_TYPE_RESERVED79,
        "Reserved (80)"	: _consts.ICMP_TYPE_RESERVED80,
        "Reserved (81)"	: _consts.ICMP_TYPE_RESERVED81,
        "Reserved (82)"	: _consts.ICMP_TYPE_RESERVED82,
        "Reserved (83)"	: _consts.ICMP_TYPE_RESERVED83,
        "Reserved (84)"	: _consts.ICMP_TYPE_RESERVED84,
        "Reserved (85)"	: _consts.ICMP_TYPE_RESERVED85,
        "Reserved (86)"	: _consts.ICMP_TYPE_RESERVED86,
        "Reserved (87)"	: _consts.ICMP_TYPE_RESERVED87,
        "Reserved (88)"	: _consts.ICMP_TYPE_RESERVED88,
        "Reserved (89)"	: _consts.ICMP_TYPE_RESERVED89,
        "Reserved (90)"	: _consts.ICMP_TYPE_RESERVED90,
        "Reserved (91)"	: _consts.ICMP_TYPE_RESERVED91,
        "Reserved (92)"	: _consts.ICMP_TYPE_RESERVED92,
        "Reserved (93)"	: _consts.ICMP_TYPE_RESERVED93,
        "Reserved (94)"	: _consts.ICMP_TYPE_RESERVED94,
        "Reserved (95)"	: _consts.ICMP_TYPE_RESERVED95,
        "Reserved (96)"	: _consts.ICMP_TYPE_RESERVED96,
        "Reserved (97)"	: _consts.ICMP_TYPE_RESERVED97,
        "Reserved (98)"	: _consts.ICMP_TYPE_RESERVED98,
        "Reserved (99)"	: _consts.ICMP_TYPE_RESERVED99,
        "Reserved (100)"	: _consts.ICMP_TYPE_RESERVED100,
        "Reserved (101)"	: _consts.ICMP_TYPE_RESERVED101,
        "Reserved (102)"	: _consts.ICMP_TYPE_RESERVED102,
        "Reserved (103)"	: _consts.ICMP_TYPE_RESERVED103,
        "Reserved (104)"	: _consts.ICMP_TYPE_RESERVED104,
        "Reserved (105)"	: _consts.ICMP_TYPE_RESERVED105,
        "Reserved (106)"	: _consts.ICMP_TYPE_RESERVED106,
        "Reserved (107)"	: _consts.ICMP_TYPE_RESERVED107,
        "Reserved (108)"	: _consts.ICMP_TYPE_RESERVED108,
        "Reserved (109)"	: _consts.ICMP_TYPE_RESERVED109,
        "Reserved (110)"	: _consts.ICMP_TYPE_RESERVED110,
        "Reserved (111)"	: _consts.ICMP_TYPE_RESERVED111,
        "Reserved (112)"	: _consts.ICMP_TYPE_RESERVED112,
        "Reserved (113)"	: _consts.ICMP_TYPE_RESERVED113,
        "Reserved (114)"	: _consts.ICMP_TYPE_RESERVED114,
        "Reserved (115)"	: _consts.ICMP_TYPE_RESERVED115,
        "Reserved (116)"	: _consts.ICMP_TYPE_RESERVED116,
        "Reserved (117)"	: _consts.ICMP_TYPE_RESERVED117,
        "Reserved (118)"	: _consts.ICMP_TYPE_RESERVED118,
        "Reserved (119)"	: _consts.ICMP_TYPE_RESERVED119,
        "Reserved (120)"	: _consts.ICMP_TYPE_RESERVED120,
        "Reserved (121)"	: _consts.ICMP_TYPE_RESERVED121,
        "Reserved (122)"	: _consts.ICMP_TYPE_RESERVED122,
        "Reserved (123)"	: _consts.ICMP_TYPE_RESERVED123,
        "Reserved (124)"	: _consts.ICMP_TYPE_RESERVED124,
        "Reserved (125)"	: _consts.ICMP_TYPE_RESERVED125,
        "Reserved (126)"	: _consts.ICMP_TYPE_RESERVED126,
        "Reserved (127)"	: _consts.ICMP_TYPE_RESERVED127,
        "Reserved (128)"	: _consts.ICMP_TYPE_RESERVED128,
        "Reserved (129)"	: _consts.ICMP_TYPE_RESERVED129,
        "Reserved (130)"	: _consts.ICMP_TYPE_RESERVED130,
        "Reserved (131)"	: _consts.ICMP_TYPE_RESERVED131,
        "Reserved (132)"	: _consts.ICMP_TYPE_RESERVED132,
        "Reserved (133)"	: _consts.ICMP_TYPE_RESERVED133,
        "Reserved (134)"	: _consts.ICMP_TYPE_RESERVED134,
        "Reserved (135)"	: _consts.ICMP_TYPE_RESERVED135,
        "Reserved (136)"	: _consts.ICMP_TYPE_RESERVED136,
        "Reserved (137)"	: _consts.ICMP_TYPE_RESERVED137,
        "Reserved (138)"	: _consts.ICMP_TYPE_RESERVED138,
        "Reserved (139)"	: _consts.ICMP_TYPE_RESERVED139,
        "Reserved (140)"	: _consts.ICMP_TYPE_RESERVED140,
        "Reserved (141)"	: _consts.ICMP_TYPE_RESERVED141,
        "Reserved (142)"	: _consts.ICMP_TYPE_RESERVED142,
        "Reserved (143)"	: _consts.ICMP_TYPE_RESERVED143,
        "Reserved (144)"	: _consts.ICMP_TYPE_RESERVED144,
        "Reserved (145)"	: _consts.ICMP_TYPE_RESERVED145,
        "Reserved (146)"	: _consts.ICMP_TYPE_RESERVED146,
        "Reserved (147)"	: _consts.ICMP_TYPE_RESERVED147,
        "Reserved (148)"	: _consts.ICMP_TYPE_RESERVED148,
        "Reserved (149)"	: _consts.ICMP_TYPE_RESERVED149,
        "Reserved (150)"	: _consts.ICMP_TYPE_RESERVED150,
        "Reserved (151)"	: _consts.ICMP_TYPE_RESERVED151,
        "Reserved (152)"	: _consts.ICMP_TYPE_RESERVED152,
        "Reserved (153)"	: _consts.ICMP_TYPE_RESERVED153,
        "Reserved (154)"	: _consts.ICMP_TYPE_RESERVED154,
        "Reserved (155)"	: _consts.ICMP_TYPE_RESERVED155,
        "Reserved (156)"	: _consts.ICMP_TYPE_RESERVED156,
        "Reserved (157)"	: _consts.ICMP_TYPE_RESERVED157,
        "Reserved (158)"	: _consts.ICMP_TYPE_RESERVED158,
        "Reserved (159)"	: _consts.ICMP_TYPE_RESERVED159,
        "Reserved (160)"	: _consts.ICMP_TYPE_RESERVED160,
        "Reserved (161)"	: _consts.ICMP_TYPE_RESERVED161,
        "Reserved (162)"	: _consts.ICMP_TYPE_RESERVED162,
        "Reserved (163)"	: _consts.ICMP_TYPE_RESERVED163,
        "Reserved (164)"	: _consts.ICMP_TYPE_RESERVED164,
        "Reserved (165)"	: _consts.ICMP_TYPE_RESERVED165,
        "Reserved (166)"	: _consts.ICMP_TYPE_RESERVED166,
        "Reserved (167)"	: _consts.ICMP_TYPE_RESERVED167,
        "Reserved (168)"	: _consts.ICMP_TYPE_RESERVED168,
        "Reserved (169)"	: _consts.ICMP_TYPE_RESERVED169,
        "Reserved (170)"	: _consts.ICMP_TYPE_RESERVED170,
        "Reserved (171)"	: _consts.ICMP_TYPE_RESERVED171,
        "Reserved (172)"	: _consts.ICMP_TYPE_RESERVED172,
        "Reserved (173)"	: _consts.ICMP_TYPE_RESERVED173,
        "Reserved (174)"	: _consts.ICMP_TYPE_RESERVED174,
        "Reserved (175)"	: _consts.ICMP_TYPE_RESERVED175,
        "Reserved (176)"	: _consts.ICMP_TYPE_RESERVED176,
        "Reserved (177)"	: _consts.ICMP_TYPE_RESERVED177,
        "Reserved (178)"	: _consts.ICMP_TYPE_RESERVED178,
        "Reserved (179)"	: _consts.ICMP_TYPE_RESERVED179,
        "Reserved (180)"	: _consts.ICMP_TYPE_RESERVED180,
        "Reserved (181)"	: _consts.ICMP_TYPE_RESERVED181,
        "Reserved (182)"	: _consts.ICMP_TYPE_RESERVED182,
        "Reserved (183)"	: _consts.ICMP_TYPE_RESERVED183,
        "Reserved (184)"	: _consts.ICMP_TYPE_RESERVED184,
        "Reserved (185)"	: _consts.ICMP_TYPE_RESERVED185,
        "Reserved (186)"	: _consts.ICMP_TYPE_RESERVED186,
        "Reserved (187)"	: _consts.ICMP_TYPE_RESERVED187,
        "Reserved (188)"	: _consts.ICMP_TYPE_RESERVED188,
        "Reserved (189)"	: _consts.ICMP_TYPE_RESERVED189,
        "Reserved (190)"	: _consts.ICMP_TYPE_RESERVED190,
        "Reserved (191)"	: _consts.ICMP_TYPE_RESERVED191,
        "Reserved (192)"	: _consts.ICMP_TYPE_RESERVED192,
        "Reserved (193)"	: _consts.ICMP_TYPE_RESERVED193,
        "Reserved (194)"	: _consts.ICMP_TYPE_RESERVED194,
        "Reserved (195)"	: _consts.ICMP_TYPE_RESERVED195,
        "Reserved (196)"	: _consts.ICMP_TYPE_RESERVED196,
        "Reserved (197)"	: _consts.ICMP_TYPE_RESERVED197,
        "Reserved (198)"	: _consts.ICMP_TYPE_RESERVED198,
        "Reserved (199)"	: _consts.ICMP_TYPE_RESERVED199,
        "Reserved (200)"	: _consts.ICMP_TYPE_RESERVED200,
        "Reserved (201)"	: _consts.ICMP_TYPE_RESERVED201,
        "Reserved (202)"	: _consts.ICMP_TYPE_RESERVED202,
        "Reserved (203)"	: _consts.ICMP_TYPE_RESERVED203,
        "Reserved (204)"	: _consts.ICMP_TYPE_RESERVED204,
        "Reserved (205)"	: _consts.ICMP_TYPE_RESERVED205,
        "Reserved (206)"	: _consts.ICMP_TYPE_RESERVED206,
        "Reserved (207)"	: _consts.ICMP_TYPE_RESERVED207,
        "Reserved (208)"	: _consts.ICMP_TYPE_RESERVED208,
        "Reserved (209)"	: _consts.ICMP_TYPE_RESERVED209,
        "Reserved (210)"	: _consts.ICMP_TYPE_RESERVED210,
        "Reserved (211)"	: _consts.ICMP_TYPE_RESERVED211,
        "Reserved (212)"	: _consts.ICMP_TYPE_RESERVED212,
        "Reserved (213)"	: _consts.ICMP_TYPE_RESERVED213,
        "Reserved (214)"	: _consts.ICMP_TYPE_RESERVED214,
        "Reserved (215)"	: _consts.ICMP_TYPE_RESERVED215,
        "Reserved (216)"	: _consts.ICMP_TYPE_RESERVED216,
        "Reserved (217)"	: _consts.ICMP_TYPE_RESERVED217,
        "Reserved (218)"	: _consts.ICMP_TYPE_RESERVED218,
        "Reserved (219)"	: _consts.ICMP_TYPE_RESERVED219,
        "Reserved (220)"	: _consts.ICMP_TYPE_RESERVED220,
        "Reserved (221)"	: _consts.ICMP_TYPE_RESERVED221,
        "Reserved (222)"	: _consts.ICMP_TYPE_RESERVED222,
        "Reserved (223)"	: _consts.ICMP_TYPE_RESERVED223,
        "Reserved (224)"	: _consts.ICMP_TYPE_RESERVED224,
        "Reserved (225)"	: _consts.ICMP_TYPE_RESERVED225,
        "Reserved (226)"	: _consts.ICMP_TYPE_RESERVED226,
        "Reserved (227)"	: _consts.ICMP_TYPE_RESERVED227,
        "Reserved (228)"	: _consts.ICMP_TYPE_RESERVED228,
        "Reserved (229)"	: _consts.ICMP_TYPE_RESERVED229,
        "Reserved (230)"	: _consts.ICMP_TYPE_RESERVED230,
        "Reserved (231)"	: _consts.ICMP_TYPE_RESERVED231,
        "Reserved (232)"	: _consts.ICMP_TYPE_RESERVED232,
        "Reserved (233)"	: _consts.ICMP_TYPE_RESERVED233,
        "Reserved (234)"	: _consts.ICMP_TYPE_RESERVED234,
        "Reserved (235)"	: _consts.ICMP_TYPE_RESERVED235,
        "Reserved (236)"	: _consts.ICMP_TYPE_RESERVED236,
        "Reserved (237)"	: _consts.ICMP_TYPE_RESERVED237,
        "Reserved (238)"	: _consts.ICMP_TYPE_RESERVED238,
        "Reserved (239)"	: _consts.ICMP_TYPE_RESERVED239,
        "Reserved (240)"	: _consts.ICMP_TYPE_RESERVED240,
        "Reserved (241)"	: _consts.ICMP_TYPE_RESERVED241,
        "Reserved (242)"	: _consts.ICMP_TYPE_RESERVED242,
        "Reserved (243)"	: _consts.ICMP_TYPE_RESERVED243,
        "Reserved (244)"	: _consts.ICMP_TYPE_RESERVED244,
        "Reserved (245)"	: _consts.ICMP_TYPE_RESERVED245,
        "Reserved (246)"	: _consts.ICMP_TYPE_RESERVED246,
        "Reserved (247)"	: _consts.ICMP_TYPE_RESERVED247,
        "Reserved (248)"	: _consts.ICMP_TYPE_RESERVED248,
        "Reserved (249)"	: _consts.ICMP_TYPE_RESERVED249,
        "Reserved (250)"	: _consts.ICMP_TYPE_RESERVED250,
        "Reserved (251)"	: _consts.ICMP_TYPE_RESERVED251,
        "Reserved (252)"	: _consts.ICMP_TYPE_RESERVED252,
        "Reserved (253)"	: _consts.ICMP_TYPE_RESERVED253,
        "Reserved (254)"	: _consts.ICMP_TYPE_RESERVED254,
        "Reserved (255)"	: _consts.ICMP_TYPE_RESERVED255,
    }

class _HCode(_fields.IntField):
    bits = 8
    auto = False

class _HChecksum(_fields.IntField):
    """
    A checksum of the ICMP protocol.
    """

    bits = 16
    auto = True
    def _generate_value(self):
        return 0

class _HExtraData(_fields.Field):
    pass

class ICMP(_protocols.Protocol):
    """
    Internet Control Message Protocol implementation.

    It the most common protocol in the Internet on fourth layer
    of the OSI model.
    """
    
    layer = 4
    protocol_id = _consts.PROTOCOL_ICMP
    name = "ICMP"

    _ordered_fields = ('type', 'code', '_checksum', '_extra_data')

    def __init__(self, **kwargs):
        """
        Create a new ICMP().
        """

        raise NotImplementedError("not finished yet")
        fields_list = [ _HType("Type"),
                        _HCode("Code"),
                        _HChecksum("Checksum"), 
                        _HExtraData("Extra Data"), ]

        super(ICMP, self).__init__(fields_list, **kwargs)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields after calling fillout() for them.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        return raw_value, bit

protocols = [ ICMP, ]
