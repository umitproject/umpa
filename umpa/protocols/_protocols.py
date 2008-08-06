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

import struct

from umpa import utils
from umpa.protocols._consts import *
from umpa.protocols._fields import Field, Flags
from umpa.utils.my_exceptions import *

class Protocol(object):
    """Superclass for protocols.
    To implement new protocol, make a subclass.
    
    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """
    _ordered_fields = ()
    layer = None
    protocol_id = None

    def __init__(self, fields_list, **kw):
        # we pack objects of header's fields to the dict
        fields = dict(zip(self._ordered_fields, fields_list))

        # because of overwritten __setattr__ we need to call super here
        self.__dict__['_fields'] = fields
        # setting up passed fields
        for field in kw:
            self.__setattr__(field, kw[field])

        self.__dict__['payload'] = None

    def __setattr__(self, attr, val):
        """Set value of the field."""

        if self._is_valid(attr):
            self._get_field(attr).set(val)
        else:
            raise UMPAAttributeException, attr + ' not allowed'

    def __getattr__(self, attr):
        """Return value of the field."""
        if self._is_valid(attr):
            return self._get_field(attr).get()
        else:
            raise UMPAAttributeException, attr + ' not allowed'

    def get_fields(self):
        """Generator for ordered fields."""
        for field in self._ordered_fields:
            yield self._get_field(field)

    @staticmethod
    def get_fields_keys():
        """Generator for ordered names (keys) of header's fields.
        
        I don't see any reason to use this method but
        Francesco asked me to make this.

        NOTE: You should use get_fields() method instead.
        """
        for field in Protocol._ordered_fields:
            yield field
    
    def _get_field(self, keyname):
        if self._is_valid(keyname):
            return self._fields[keyname]
        else:
            raise UMPAAttributeException, keyname + ' not allowed'

    def set_fields(self, *args, **kwargs):
        """Set fields of the protocol.
        There are 2 ways to do that with using tuple or dict-style.
        """
        # converting args list to the dict and update our kwargs
        kwargs.update(utils.dict_from_sequence(args))

        for key in kwargs:
            if self._is_valid(key):
                setattr(self, key, kwargs[key])
            self.fields[key].set(kwargs[key])

    def set_flags(self, name, *args, **kw):
        """Set flags with dict using.

        There are 2 ways to do that with using tuple or dict-style.

        There is no effect if the protocol doesn't have this field.
        """

        # converting args list to the dict and update our kwargs
        kw.update(utils.dict_from_sequence(args))

        flag_field = self._get_field(name)
        if isinstance(flag_field, Flags):
            for flag_name in kw:
                if kw[flag_name]:
                    flag_field.set(flag_name)
                else:
                    flag_field.unset(flag_name)
        else:
            raise UMPAAttributeException, "No Flags instance for " + name

    def get_flags(self, name, *args):
        flag_field = self._get_field(name)
        if isinstance(flag_field, Flags):
            return flag_field.get(*args)
        else:
            raise UMPAAttributeException, "No Flags instance for " + name

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        raise NotImplementedError, "this is abstract class"

    def _raw(self, raw_value, bit, protocol_container, protocol_bits):
        raw_value = 0
        bit = 0
        # because of some protocols implementation, there are some tasks before
        # we call fillout() for fields
        raw_value, bit = self._pre_raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        # so we make a big number with bits of every fields of the protocol
        for field in reversed(self._ordered_fields):
            x = self._get_field(field).fillout()
            raw_value |= x << bit
            bit += self._get_field(field).bits

        # because of some protocols implementation, there are some tasks after
        # we call fillout() for fields
        raw_value, bit = self._post_raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        raise NotImplementedError, "this is abstract class"

    def _get_raw(self, protocol_container, protocol_bits):
        """Return raw bits of the protocol's object."""

        raw_value = 0
        bit = 0
        # The deal: we join all value's fields into one big number
        # (with taking care about amount of bits).
        # then we devide the number on byte-chunks
        # and pack it by struct.pack() function
        raw_value, bit = self._raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        # protocol should return byte-compatible length
        if bit%BYTE != 0:
            raise UMPAException, 'odd number of bits in ' + self.__name__

        return raw_value, bit

    def _is_valid(self, field):
        """Check if attribute is allowed."""
        return self._fields.has_key(field)

    def get_offset(self, field):
        """Return offset for the field.
        
        NOTE: the argument field CAN be key or instance.
        """

        # checking if argument is a key or instance
        if isinstance(field, str):
            field_list = self._ordered_fields
        elif isinstance(field, Field):
            field_list = [ f for f in self.get_fields() ]
        else:
            raise UMPAException, type(field) + ' unsupported'
    
        if field not in field_list:
            raise UMPAAttributeException, field + ' not allowed'

        offset = 0
        for i, f in enumerate(field_list):
            if field == f:
                break
            offset += self._get_field(self._ordered_fields[i]).bits
        return offset
