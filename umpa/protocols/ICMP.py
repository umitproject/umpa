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

import umpa.protocols._consts as const

from umpa.protocols._fields import *
from umpa.protocols._protocols import *

class HType(EnumIntField):
    bits = 8
    auto = False
    enumerable = {
        "Echo Reply"	: const.ICMP_TYPE_ECHO_REPLY =  (0),
        "Unassigned (1)"	: const.ICMP_TYPE_UNASSIGNED1 = 1,
        "Unassigned (2)"	: const.ICMP_TYPE_UNASSIGNED2 = 2,
        "Destination Unreachable"	: const.ICMP_TYPE_DESTINATION_UNREACHABLE =  (3),
        "Source Quench"	: const.ICMP_TYPE_SOURCE_QUENCH =  (4),
        "Redirect"	: const.ICMP_TYPE_REDIRECT =  (5),
        "Alternate Host Address"	: const.ICMP_TYPE_ALTERNATE_HOST_ADDRESS =  (6),
        "Unassigned (7)"	: const.ICMP_TYPE_UNASSIGNED7 = 7,
        "Echo"	: const.ICMP_TYPE_ECHO =  (8),
        "Router Advertisement"	: const.ICMP_TYPE_ROUTER_ADVERTISEMENT =  (9),
        "Router Solicitation"	: const.ICMP_TYPE_ROUTER_SOLICITATION =  (10),
        "Time Exceeded"	: const.ICMP_TYPE_TIME_EXCEEDED =  (11),
        "Parameter Problem"	: const.ICMP_TYPE_PARAMETER_PROBLEM =  (12),
        "Timestamp"	: const.ICMP_TYPE_TIMESTAMP =  (13),
        "Timestamp Reply"	: const.ICMP_TYPE_TIMESTAMP_REPLY =  (14),
        "Information Request"	: const.ICMP_TYPE_INFORMATION_REQUEST =  (15),
        "Information Reply"	: const.ICMP_TYPE_INFORMATION_REPLY =  (16),
        "Address Mask Request"	: const.ICMP_TYPE_ADDRESS_MASK_REQUEST =  (17),
        "Address Mask Reply"	: const.ICMP_TYPE_ADDRESS_MASK_REPLY =  (18),
        "Reserved Security"	: const.ICMP_TYPE_RESERVED_SECURITY =  (19),
        "Reserved Robustness"	: const.ICMP_TYPE_RESERVED_ROBUSTNESS =  (29),
        "Traceroute"	: const.ICMP_TYPE_TRACEROUTE =  (30),
        "Datagram Conversion Error"	: const.ICMP_TYPE_DATAGRAM_CONVERSION_ERROR =  (31),
        "Mobile Host Redirect"	: const.ICMP_TYPE_MOBILE_HOST_REDIRECT =  (32),
        "Ipv (6) Where-Are-You"	: const.ICMP_TYPE_IPV6_WHERE-ARE-YOU = 33,
        "Ipv (6) I-Am-Here"	: const.ICMP_TYPE_IPV6_I-AM-HERE = 34,
        "Mobile Registration Request"	: const.ICMP_TYPE_MOBILE_REGISTRATION_REQUEST =  (35),
        "Mobile Registration Reply"	: const.ICMP_TYPE_MOBILE_REGISTRATION_REPLY =  (36),
        "Domain Name Request"	: const.ICMP_TYPE_DOMAIN_NAME_REQUEST =  (37),
        "Domain Name Reply"	: const.ICMP_TYPE_DOMAIN_NAME_REPLY =  (38),
        "Skip"	: const.ICMP_TYPE_SKIP =  (39),
        "Photuris"	: const.ICMP_TYPE_PHOTURIS =  (40),
        "Icmp Messages Utilized"	: const.ICMP_TYPE_ICMP_MESSAGES_UTILIZED =  (41),
        "Reserved (42)"	: const.ICMP_TYPE_RESERVED42 = 42,
        "Reserved (43)"	: const.ICMP_TYPE_RESERVED43 = 43,
        "Reserved (44)"	: const.ICMP_TYPE_RESERVED44 = 44,
        "Reserved (45)"	: const.ICMP_TYPE_RESERVED45 = 45,
        "Reserved (46)"	: const.ICMP_TYPE_RESERVED46 = 46,
        "Reserved (47)"	: const.ICMP_TYPE_RESERVED47 = 47,
        "Reserved (48)"	: const.ICMP_TYPE_RESERVED48 = 48,
        "Reserved (49)"	: const.ICMP_TYPE_RESERVED49 = 49,
        "Reserved (50)"	: const.ICMP_TYPE_RESERVED50 = 50,
        "Reserved (51)"	: const.ICMP_TYPE_RESERVED51 = 51,
        "Reserved (52)"	: const.ICMP_TYPE_RESERVED52 = 52,
        "Reserved (53)"	: const.ICMP_TYPE_RESERVED53 = 53,
        "Reserved (54)"	: const.ICMP_TYPE_RESERVED54 = 54,
        "Reserved (55)"	: const.ICMP_TYPE_RESERVED55 = 55,
        "Reserved (56)"	: const.ICMP_TYPE_RESERVED56 = 56,
        "Reserved (57)"	: const.ICMP_TYPE_RESERVED57 = 57,
        "Reserved (58)"	: const.ICMP_TYPE_RESERVED58 = 58,
        "Reserved (59)"	: const.ICMP_TYPE_RESERVED59 = 59,
        "Reserved (60)"	: const.ICMP_TYPE_RESERVED60 = 60,
        "Reserved (61)"	: const.ICMP_TYPE_RESERVED61 = 61,
        "Reserved (62)"	: const.ICMP_TYPE_RESERVED62 = 62,
        "Reserved (63)"	: const.ICMP_TYPE_RESERVED63 = 63,
        "Reserved (64)"	: const.ICMP_TYPE_RESERVED64 = 64,
        "Reserved (65)"	: const.ICMP_TYPE_RESERVED65 = 65,
        "Reserved (66)"	: const.ICMP_TYPE_RESERVED66 = 66,
        "Reserved (67)"	: const.ICMP_TYPE_RESERVED67 = 67,
        "Reserved (68)"	: const.ICMP_TYPE_RESERVED68 = 68,
        "Reserved (69)"	: const.ICMP_TYPE_RESERVED69 = 69,
        "Reserved (70)"	: const.ICMP_TYPE_RESERVED70 = 70,
        "Reserved (71)"	: const.ICMP_TYPE_RESERVED71 = 71,
        "Reserved (72)"	: const.ICMP_TYPE_RESERVED72 = 72,
        "Reserved (73)"	: const.ICMP_TYPE_RESERVED73 = 73,
        "Reserved (74)"	: const.ICMP_TYPE_RESERVED74 = 74,
        "Reserved (75)"	: const.ICMP_TYPE_RESERVED75 = 75,
        "Reserved (76)"	: const.ICMP_TYPE_RESERVED76 = 76,
        "Reserved (77)"	: const.ICMP_TYPE_RESERVED77 = 77,
        "Reserved (78)"	: const.ICMP_TYPE_RESERVED78 = 78,
        "Reserved (79)"	: const.ICMP_TYPE_RESERVED79 = 79,
        "Reserved (80)"	: const.ICMP_TYPE_RESERVED80 = 80,
        "Reserved (81)"	: const.ICMP_TYPE_RESERVED81 = 81,
        "Reserved (82)"	: const.ICMP_TYPE_RESERVED82 = 82,
        "Reserved (83)"	: const.ICMP_TYPE_RESERVED83 = 83,
        "Reserved (84)"	: const.ICMP_TYPE_RESERVED84 = 84,
        "Reserved (85)"	: const.ICMP_TYPE_RESERVED85 = 85,
        "Reserved (86)"	: const.ICMP_TYPE_RESERVED86 = 86,
        "Reserved (87)"	: const.ICMP_TYPE_RESERVED87 = 87,
        "Reserved (88)"	: const.ICMP_TYPE_RESERVED88 = 88,
        "Reserved (89)"	: const.ICMP_TYPE_RESERVED89 = 89,
        "Reserved (90)"	: const.ICMP_TYPE_RESERVED90 = 90,
        "Reserved (91)"	: const.ICMP_TYPE_RESERVED91 = 91,
        "Reserved (92)"	: const.ICMP_TYPE_RESERVED92 = 92,
        "Reserved (93)"	: const.ICMP_TYPE_RESERVED93 = 93,
        "Reserved (94)"	: const.ICMP_TYPE_RESERVED94 = 94,
        "Reserved (95)"	: const.ICMP_TYPE_RESERVED95 = 95,
        "Reserved (96)"	: const.ICMP_TYPE_RESERVED96 = 96,
        "Reserved (97)"	: const.ICMP_TYPE_RESERVED97 = 97,
        "Reserved (98)"	: const.ICMP_TYPE_RESERVED98 = 98,
        "Reserved (99)"	: const.ICMP_TYPE_RESERVED99 = 99,
        "Reserved (100)"	: const.ICMP_TYPE_RESERVED100 = 100,
        "Reserved (101)"	: const.ICMP_TYPE_RESERVED101 = 101,
        "Reserved (102)"	: const.ICMP_TYPE_RESERVED102 = 102,
        "Reserved (103)"	: const.ICMP_TYPE_RESERVED103 = 103,
        "Reserved (104)"	: const.ICMP_TYPE_RESERVED104 = 104,
        "Reserved (105)"	: const.ICMP_TYPE_RESERVED105 = 105,
        "Reserved (106)"	: const.ICMP_TYPE_RESERVED106 = 106,
        "Reserved (107)"	: const.ICMP_TYPE_RESERVED107 = 107,
        "Reserved (108)"	: const.ICMP_TYPE_RESERVED108 = 108,
        "Reserved (109)"	: const.ICMP_TYPE_RESERVED109 = 109,
        "Reserved (110)"	: const.ICMP_TYPE_RESERVED110 = 110,
        "Reserved (111)"	: const.ICMP_TYPE_RESERVED111 = 111,
        "Reserved (112)"	: const.ICMP_TYPE_RESERVED112 = 112,
        "Reserved (113)"	: const.ICMP_TYPE_RESERVED113 = 113,
        "Reserved (114)"	: const.ICMP_TYPE_RESERVED114 = 114,
        "Reserved (115)"	: const.ICMP_TYPE_RESERVED115 = 115,
        "Reserved (116)"	: const.ICMP_TYPE_RESERVED116 = 116,
        "Reserved (117)"	: const.ICMP_TYPE_RESERVED117 = 117,
        "Reserved (118)"	: const.ICMP_TYPE_RESERVED118 = 118,
        "Reserved (119)"	: const.ICMP_TYPE_RESERVED119 = 119,
        "Reserved (120)"	: const.ICMP_TYPE_RESERVED120 = 120,
        "Reserved (121)"	: const.ICMP_TYPE_RESERVED121 = 121,
        "Reserved (122)"	: const.ICMP_TYPE_RESERVED122 = 122,
        "Reserved (123)"	: const.ICMP_TYPE_RESERVED123 = 123,
        "Reserved (124)"	: const.ICMP_TYPE_RESERVED124 = 124,
        "Reserved (125)"	: const.ICMP_TYPE_RESERVED125 = 125,
        "Reserved (126)"	: const.ICMP_TYPE_RESERVED126 = 126,
        "Reserved (127)"	: const.ICMP_TYPE_RESERVED127 = 127,
        "Reserved (128)"	: const.ICMP_TYPE_RESERVED128 = 128,
        "Reserved (129)"	: const.ICMP_TYPE_RESERVED129 = 129,
        "Reserved (130)"	: const.ICMP_TYPE_RESERVED130 = 130,
        "Reserved (131)"	: const.ICMP_TYPE_RESERVED131 = 131,
        "Reserved (132)"	: const.ICMP_TYPE_RESERVED132 = 132,
        "Reserved (133)"	: const.ICMP_TYPE_RESERVED133 = 133,
        "Reserved (134)"	: const.ICMP_TYPE_RESERVED134 = 134,
        "Reserved (135)"	: const.ICMP_TYPE_RESERVED135 = 135,
        "Reserved (136)"	: const.ICMP_TYPE_RESERVED136 = 136,
        "Reserved (137)"	: const.ICMP_TYPE_RESERVED137 = 137,
        "Reserved (138)"	: const.ICMP_TYPE_RESERVED138 = 138,
        "Reserved (139)"	: const.ICMP_TYPE_RESERVED139 = 139,
        "Reserved (140)"	: const.ICMP_TYPE_RESERVED140 = 140,
        "Reserved (141)"	: const.ICMP_TYPE_RESERVED141 = 141,
        "Reserved (142)"	: const.ICMP_TYPE_RESERVED142 = 142,
        "Reserved (143)"	: const.ICMP_TYPE_RESERVED143 = 143,
        "Reserved (144)"	: const.ICMP_TYPE_RESERVED144 = 144,
        "Reserved (145)"	: const.ICMP_TYPE_RESERVED145 = 145,
        "Reserved (146)"	: const.ICMP_TYPE_RESERVED146 = 146,
        "Reserved (147)"	: const.ICMP_TYPE_RESERVED147 = 147,
        "Reserved (148)"	: const.ICMP_TYPE_RESERVED148 = 148,
        "Reserved (149)"	: const.ICMP_TYPE_RESERVED149 = 149,
        "Reserved (150)"	: const.ICMP_TYPE_RESERVED150 = 150,
        "Reserved (151)"	: const.ICMP_TYPE_RESERVED151 = 151,
        "Reserved (152)"	: const.ICMP_TYPE_RESERVED152 = 152,
        "Reserved (153)"	: const.ICMP_TYPE_RESERVED153 = 153,
        "Reserved (154)"	: const.ICMP_TYPE_RESERVED154 = 154,
        "Reserved (155)"	: const.ICMP_TYPE_RESERVED155 = 155,
        "Reserved (156)"	: const.ICMP_TYPE_RESERVED156 = 156,
        "Reserved (157)"	: const.ICMP_TYPE_RESERVED157 = 157,
        "Reserved (158)"	: const.ICMP_TYPE_RESERVED158 = 158,
        "Reserved (159)"	: const.ICMP_TYPE_RESERVED159 = 159,
        "Reserved (160)"	: const.ICMP_TYPE_RESERVED160 = 160,
        "Reserved (161)"	: const.ICMP_TYPE_RESERVED161 = 161,
        "Reserved (162)"	: const.ICMP_TYPE_RESERVED162 = 162,
        "Reserved (163)"	: const.ICMP_TYPE_RESERVED163 = 163,
        "Reserved (164)"	: const.ICMP_TYPE_RESERVED164 = 164,
        "Reserved (165)"	: const.ICMP_TYPE_RESERVED165 = 165,
        "Reserved (166)"	: const.ICMP_TYPE_RESERVED166 = 166,
        "Reserved (167)"	: const.ICMP_TYPE_RESERVED167 = 167,
        "Reserved (168)"	: const.ICMP_TYPE_RESERVED168 = 168,
        "Reserved (169)"	: const.ICMP_TYPE_RESERVED169 = 169,
        "Reserved (170)"	: const.ICMP_TYPE_RESERVED170 = 170,
        "Reserved (171)"	: const.ICMP_TYPE_RESERVED171 = 171,
        "Reserved (172)"	: const.ICMP_TYPE_RESERVED172 = 172,
        "Reserved (173)"	: const.ICMP_TYPE_RESERVED173 = 173,
        "Reserved (174)"	: const.ICMP_TYPE_RESERVED174 = 174,
        "Reserved (175)"	: const.ICMP_TYPE_RESERVED175 = 175,
        "Reserved (176)"	: const.ICMP_TYPE_RESERVED176 = 176,
        "Reserved (177)"	: const.ICMP_TYPE_RESERVED177 = 177,
        "Reserved (178)"	: const.ICMP_TYPE_RESERVED178 = 178,
        "Reserved (179)"	: const.ICMP_TYPE_RESERVED179 = 179,
        "Reserved (180)"	: const.ICMP_TYPE_RESERVED180 = 180,
        "Reserved (181)"	: const.ICMP_TYPE_RESERVED181 = 181,
        "Reserved (182)"	: const.ICMP_TYPE_RESERVED182 = 182,
        "Reserved (183)"	: const.ICMP_TYPE_RESERVED183 = 183,
        "Reserved (184)"	: const.ICMP_TYPE_RESERVED184 = 184,
        "Reserved (185)"	: const.ICMP_TYPE_RESERVED185 = 185,
        "Reserved (186)"	: const.ICMP_TYPE_RESERVED186 = 186,
        "Reserved (187)"	: const.ICMP_TYPE_RESERVED187 = 187,
        "Reserved (188)"	: const.ICMP_TYPE_RESERVED188 = 188,
        "Reserved (189)"	: const.ICMP_TYPE_RESERVED189 = 189,
        "Reserved (190)"	: const.ICMP_TYPE_RESERVED190 = 190,
        "Reserved (191)"	: const.ICMP_TYPE_RESERVED191 = 191,
        "Reserved (192)"	: const.ICMP_TYPE_RESERVED192 = 192,
        "Reserved (193)"	: const.ICMP_TYPE_RESERVED193 = 193,
        "Reserved (194)"	: const.ICMP_TYPE_RESERVED194 = 194,
        "Reserved (195)"	: const.ICMP_TYPE_RESERVED195 = 195,
        "Reserved (196)"	: const.ICMP_TYPE_RESERVED196 = 196,
        "Reserved (197)"	: const.ICMP_TYPE_RESERVED197 = 197,
        "Reserved (198)"	: const.ICMP_TYPE_RESERVED198 = 198,
        "Reserved (199)"	: const.ICMP_TYPE_RESERVED199 = 199,
        "Reserved (200)"	: const.ICMP_TYPE_RESERVED200 = 200,
        "Reserved (201)"	: const.ICMP_TYPE_RESERVED201 = 201,
        "Reserved (202)"	: const.ICMP_TYPE_RESERVED202 = 202,
        "Reserved (203)"	: const.ICMP_TYPE_RESERVED203 = 203,
        "Reserved (204)"	: const.ICMP_TYPE_RESERVED204 = 204,
        "Reserved (205)"	: const.ICMP_TYPE_RESERVED205 = 205,
        "Reserved (206)"	: const.ICMP_TYPE_RESERVED206 = 206,
        "Reserved (207)"	: const.ICMP_TYPE_RESERVED207 = 207,
        "Reserved (208)"	: const.ICMP_TYPE_RESERVED208 = 208,
        "Reserved (209)"	: const.ICMP_TYPE_RESERVED209 = 209,
        "Reserved (210)"	: const.ICMP_TYPE_RESERVED210 = 210,
        "Reserved (211)"	: const.ICMP_TYPE_RESERVED211 = 211,
        "Reserved (212)"	: const.ICMP_TYPE_RESERVED212 = 212,
        "Reserved (213)"	: const.ICMP_TYPE_RESERVED213 = 213,
        "Reserved (214)"	: const.ICMP_TYPE_RESERVED214 = 214,
        "Reserved (215)"	: const.ICMP_TYPE_RESERVED215 = 215,
        "Reserved (216)"	: const.ICMP_TYPE_RESERVED216 = 216,
        "Reserved (217)"	: const.ICMP_TYPE_RESERVED217 = 217,
        "Reserved (218)"	: const.ICMP_TYPE_RESERVED218 = 218,
        "Reserved (219)"	: const.ICMP_TYPE_RESERVED219 = 219,
        "Reserved (220)"	: const.ICMP_TYPE_RESERVED220 = 220,
        "Reserved (221)"	: const.ICMP_TYPE_RESERVED221 = 221,
        "Reserved (222)"	: const.ICMP_TYPE_RESERVED222 = 222,
        "Reserved (223)"	: const.ICMP_TYPE_RESERVED223 = 223,
        "Reserved (224)"	: const.ICMP_TYPE_RESERVED224 = 224,
        "Reserved (225)"	: const.ICMP_TYPE_RESERVED225 = 225,
        "Reserved (226)"	: const.ICMP_TYPE_RESERVED226 = 226,
        "Reserved (227)"	: const.ICMP_TYPE_RESERVED227 = 227,
        "Reserved (228)"	: const.ICMP_TYPE_RESERVED228 = 228,
        "Reserved (229)"	: const.ICMP_TYPE_RESERVED229 = 229,
        "Reserved (230)"	: const.ICMP_TYPE_RESERVED230 = 230,
        "Reserved (231)"	: const.ICMP_TYPE_RESERVED231 = 231,
        "Reserved (232)"	: const.ICMP_TYPE_RESERVED232 = 232,
        "Reserved (233)"	: const.ICMP_TYPE_RESERVED233 = 233,
        "Reserved (234)"	: const.ICMP_TYPE_RESERVED234 = 234,
        "Reserved (235)"	: const.ICMP_TYPE_RESERVED235 = 235,
        "Reserved (236)"	: const.ICMP_TYPE_RESERVED236 = 236,
        "Reserved (237)"	: const.ICMP_TYPE_RESERVED237 = 237,
        "Reserved (238)"	: const.ICMP_TYPE_RESERVED238 = 238,
        "Reserved (239)"	: const.ICMP_TYPE_RESERVED239 = 239,
        "Reserved (240)"	: const.ICMP_TYPE_RESERVED240 = 240,
        "Reserved (241)"	: const.ICMP_TYPE_RESERVED241 = 241,
        "Reserved (242)"	: const.ICMP_TYPE_RESERVED242 = 242,
        "Reserved (243)"	: const.ICMP_TYPE_RESERVED243 = 243,
        "Reserved (244)"	: const.ICMP_TYPE_RESERVED244 = 244,
        "Reserved (245)"	: const.ICMP_TYPE_RESERVED245 = 245,
        "Reserved (246)"	: const.ICMP_TYPE_RESERVED246 = 246,
        "Reserved (247)"	: const.ICMP_TYPE_RESERVED247 = 247,
        "Reserved (248)"	: const.ICMP_TYPE_RESERVED248 = 248,
        "Reserved (249)"	: const.ICMP_TYPE_RESERVED249 = 249,
        "Reserved (250)"	: const.ICMP_TYPE_RESERVED250 = 250,
        "Reserved (251)"	: const.ICMP_TYPE_RESERVED251 = 251,
        "Reserved (252)"	: const.ICMP_TYPE_RESERVED252 = 252,
        "Reserved (253)"	: const.ICMP_TYPE_RESERVED253 = 253,
        "Reserved (254)"	: const.ICMP_TYPE_RESERVED254 = 254,
        "Reserved (255)"	: const.ICMP_TYPE_RESERVED255 = 255,
    }

class HCode(IntField):
    bits = 8
    auto = False

class HChecksum(IntField):
    bits = 16
    auto = True
    def _generate_value(self):
        return 0

class HExtraData(Field):
    pass

class ICMP(Protocol):
    layer = 4
    protocol_id = const.PROTOCOL_ICMP
    name = "ICMP"

    _ordered_fields = ('type', 'code', '_checksum', '_extra_data')

    def __init__(self, **kw):
        raise NotImplementedError("not finished yet")
        fields_list = [ HType("Type"), HCode("Code"), HChecksum("Checksum"), 
                        HExtraData("Extra Data"), ]

        super(ICMP, self).__init__(fields_list, **kw)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit

protocols = [ ICMP, ]
