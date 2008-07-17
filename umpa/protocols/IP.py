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

import base

from base import Field, Flags
from umpa.utils.my_exceptions import UMPAAttributeException

class HIHL(base.Field):
    _bits = 4
    def fillout(self):
        pass

class HTotalLength(base.Field):
    _bits = 16
    def fillout(self):
        pass

class HIdentification(base.Field):
    _bits = 16
    def fillout(self):
        pass

class HFragmentOffset(base.Field):
    _bits = 13
    def fillout(self):
        pass

class HProtocol(base.Field):
    _bits = 8
    def fillout(self):
        pass

class HHeaderChecksum(base.Field):
    _bits = 16
    def fillout(self):
        pass

class HPadding(base.Field):
    _bits = 0
    def fillout(self):
        pass

# main IP class

class IP(base.Protocol):
    _ordered_fields = ('_version', '_ihl', 'type_of_service', '_total_length',
                        '_identification', 'flags', '_fragment_offset',
                        'time_to_live', '_protocol', '_header_checksum',
                        'source_address', 'destination_address', 'options',
                        '_padding',)

    def __init__(self, **kw):
        base.Protocol.__init__(self, kw)

        self.layer = 3      # layer of OSI

        tos = ('presedence0','presedence1', 'presedence2', 'delay',
                'throughput', 'relibility', 'reserved0', 'reserverd1')
        flags = ('reserved', 'df', 'mf')

        fields_list = [ Field(4, 4), HIHL(), Flags(tos), HTotalLength(),
                        HIdentification(), Flags(flags, reserved=0),
                        HFragmentOffset(), Field(255, 8), HProtocol(),
                        HHeaderChecksum(), Field(bits=16), Field(bits=16),
                        Flags(()), HPadding() ]

        # we pack objects of header's fields to the dict
        self._fields = dict(zip(self._ordered_list, fields_list))

        # setting up passed fields
        for field in kw:
            self.__setattr__(field, kw[field])

    def _is_valid(self, name):
        """Check if attribute is allowed."""
        return self._fields.has_key(name)

    def __setattr__(self, attr, val):
        """Set value of the field."""

        # we can do the same without _is_valid() with just try/except section
        # but Francesco asked me about this method
        if self._is_valid(attr):
            self._fields[attr].set(val)
        else:
            raise UMPAAttributeException, attr + ' not allowed'

    def __getattr__(self, attr):
        """Return value of the field."""
        if self._is_valid(attr):
            return self._fields[attr].get()
        else:
            raise UMPAAttributeException, attr + ' not allowed'
