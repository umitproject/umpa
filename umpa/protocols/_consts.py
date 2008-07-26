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

# IP Versions
IPVERSION_4 = 4
IPVERSION_6 = 6

# Protocol Numbers (based on RFC 790 "Assigned Numbers")
PROTOCOL_ICMP = 1
PROTOCOL_TCP = 6
PROTOCOL_UDP = 17

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
