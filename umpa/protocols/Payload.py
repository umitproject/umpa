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

from umpa.protocols import *
from umpa.protocols._consts import BYTE

class HData(Field): # FIXME: should we move it to _fields.py as a common field?
    """Data as a strings.
    """
    bits = 0
    auto = False

    def _is_valid(self, val):
        return True     # we use str() so everything is ok

    def set(self, value):
        if self._is_valid(value):
            self._value = str(value)    # converting to str

            # calculate how many bits we need
            self.bits = len(self._value) * BYTE
        else:
            raise UMPAAttributeException, value + ' not allowed'

    def clear(self):
        super(Field, self).lear()
        self.bits = 0

    def _raw_value(self):
        raw = 0
        for char in self._value:
            raw += ord(char)
            raw <<= BYTE
        raw >>= BYTE

        return raw

class Payload(Protocol):
    """Use this as a protocol upper 4th layer of OSI model.
    """
    layer = 5
    name = "Payload"
    _ordered_fields = ('data',)

    def __init__(self, **kw):
        fields_list = [ HData("Data"), ]

        super(Payload, self).__init__(fields_list, **kw)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit

protocols = [ Payload, ]
