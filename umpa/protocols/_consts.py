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

BYTE = 8

# Ether types (based on IEEE 802.1Q)
ETHERTYPE_ARP = 0x0806
ETHERTYPE_RARP = 0x8035
ETHERTYPE_IP = 0x0800
ETHERTYPE_IPV6 = 0x86DD
ETHERTYPE_PPPOE = 0x8863

# IP Versions (based on RFC 790 "Assigned Numbers")
IPVERSION_RESERVED0 = 0
IPVERSION_4 = 4
IPVERSION_ST_DATAGRAM_MODE = 5
IPVERSION_6 = 6
IPVERSION_RESERVED15 = 15

# Protocol Numbers (based on RFC 790 "Assigned Numbers")
PROTOCOL_RESERVED0 = 0
PROTOCOL_ICMP = 1
PROTOCOL_GATEWAY_TO_GATEWAY = 3
PROTOCOL_CMCC = 4
PROTOCOL_ST = 5
PROTOCOL_TCP = 6
PROTOCOL_UCL = 7
PROTOCOL_SECURE = 9
PROTOCOL_BBN_RCC_MONITORING = 10
PROTOCOL_NVP = 11
PROTOCOL_PUP = 12
PROTOCOL_PLURIBUS = 13
PROTOCOL_TELENET = 14
PROTOCOL_XNET = 15
PROTOCOL_CHAOS = 16
PROTOCOL_UDP = 17
PROTOCOL_MULTIPLEXING = 18
PROTOCOL_DCN = 19
PROTOCOL_TAC_MONITORING = 20
PROTOCOL_ANY = 63
PROTOCOL_SATNET_BACKROOM_EXPAK = 64
PROTOCOL_MIT_SUBNET_SUPPORT = 65
PROTOCOL_SATNET_MONITORING = 69
PROTOCOL_INTERNET_PACKET_CORE_UTILITY = 71
PROTOCOL_BACKROOM_SATNET_MONITORING = 76
PROTOCOL_WIDEBAND_MONITORING = 78
PROTOCOL_WIDEBAND_EXPAK = 79
PROTOCOL_RESERVED255 = 255

# TTL initial values
# based on http://secfr.nerim.net/docs/fingerprint/en/ttl_default.html
TTL_AIX = 60
TTL_DEC = 30
TTL_FREEBSD = 64
TTL_HPUX = 64
TTL_IRIX = 60
TTL_LINUX = 64
TTL_MACOS = 60
TTL_OS2 = 64
TTL_SOLARIS = 255
TTL_SUNOS = 60
TTL_ULTRIX = 60
TTL_WINDOWS = 128
