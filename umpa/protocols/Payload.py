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
Payload "protocol" implementation.

Payload is the abstract protocol of 5-7 layers of the OSI model.
"""

from umpa.protocols._fields import Field
from umpa.protocols._protocols import Protocol
from umpa.protocols._consts import BYTE

from umpa.utils.exceptions import UMPAAttributeException

__all__ = [ "Payload", ]

class _HData(Field):
    """
    Data as a strings.
    """
    
    bits = 0
    auto = False

    def set(self, value):
        """
        Set the new value of the field.

        @param value: assign new value with str() casting.
        """
        if self._is_valid(value):
            self._value = str(value)    # converting to str

            # calculate how many bits we need
            self.bits = len(self._value) * BYTE
        else:
            raise UMPAAttributeException(value + ' is not allowed')

    def clear(self):
        """
        Clear the current value of the field.
        """

        super(_HData, self).clear()
        self.bits = 0

    def _is_valid(self, val):
        """
        Validate if the value is not bigger than expected.

        @param val: the new value.

        @rtype: C{bool}
        @return: C{True}.
        """
        return True     # we use str() so everything is ok

    def _raw_value(self):
        """
        Convert the value to the raw mode.

        Convert every character into the integer ordinal.
        Merge the integer values.
        Raw value's type is a number. It has to be in big-endian order.
        The bits of the result of this method are inserted into the raw number
        of the whole protocol.

        @rtype: C{number}
        @return: raw value of the field.
        """

        raw = 0
        for char in self._value:
            raw += ord(char)
            raw <<= BYTE
        raw >>= BYTE

        return raw

class Payload(Protocol):
    """
    Payload -- data of 5-7 layers of the OSI model.
    """

    layer = 5
    name = "Payload"
    _ordered_fields = ('data',)

    def __init__(self, payload=None, **kwargs):
        """
        Create a new Payload().

        @type payload: C{str}
        @param payload: data for the protocol

        @param kwargs: pass to super-constructor.

        @note: payload can be passed as a first argument (payload)
        or as a keyword (data=). if both, then keyword data overwrite
        former argument.
        """

        fields_list = [ _HData("Data"), ]

        if payload is not None and 'data' not in kwargs:
            kwargs['data'] = payload

        super(Payload, self).__init__(fields_list, **kwargs)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        Nothing to do for Payload class here. Return required vars.

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

        Nothing to do for Payload class here. Return required vars.

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

protocols = [ Payload, ]
