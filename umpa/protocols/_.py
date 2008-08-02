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
from umpa.utils.my_exceptions import *

class Field(object):
    """Superclass for fields.
    To implement new fields, create subclass of this.

    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """
    bits = 0
    auto = False
    def __init__(self, name, value=None, bits=None, auto=None):
        self.name = name
        if auto:
            self.auto = auto
        elif value:
            self.auto = True    # if there's default value, auto should be True

        if bits:
            self.bits = bits
        self._value = value
        # _modified is logical attribute to have easy access if user
        # modified the value. it's helpful for autofilling fields
        self._modified = False

    def set(self, value):
        if self._is_valid(value):
            self._value = value
            self._modified = True
        else:
            raise UMPAAttributeException, value + ' not allowed'

    def get(self):
        return self._value

    def clear(self):
        self._value = None
        self._modified = False

    def set_doc(self, text):
        self.__doc__ = text

    def _is_valid(self, val):
        raise NotImplementedError, "this is abstract class"

    def _pre_fillout(self):
        pass

    def _raw_value(self):
        raise NotImplementedError, "this is abstract class"

    def _generate_value(self):
        raise UMPAException, "value is not defined or _generate_value() \
                                            method is not implemented."

    def fillout(self, *args):
        self._pre_fillout()

        # we have to clear self._value if it was not defined
        # because of later usage
        if not self._value:
            self._value = self._generate_value()
            raw = self._raw_value()
            self.clear()
        else:
            raw = self._raw_value()
        
        return raw

    def _check_related_field(self, raw_value, bits_raw, offset):
        temp_value = ( raw >> bits_raw - offset - self.bits) \
                                                    & ( 1 << self.bits ) - 1
        if temp_value == AUTOFILL_DEFAULT and self.default:
            return True
        else:
            return False

class IntField(Field):
    def _raw_value(self):
        return self._value

    def _is_valid(self, val):
        """Check if a value is not bigger than expected.
        """

        if 2**self.bits > val:
            return True
        else:
            return False

class AddrField(Field):
    pass

class IPAddrField(AddrField):
    """Main class for IP-style adresses.
    It handles with 2 types of data:
    1 - strings as "127.0.0.1" or "0:0:0:0:0:0:0:1"
    2 - tuples as (127,0,0,1) or (0,0,0,0,0,0,0,1)
    """
    def set(self, value):
        # convert list to tuple
        if type(value) is list:
            value = tuple(value)

        super(IPAddrField, self).set(value)

    def _raw_value(self):
        if type(self._value) is str:
            pieces = self._value.split(self.separator)
        else:
            pieces = self._value

        raw = 0
        for b in pieces:
            raw += int(b, self.base)
            raw <<= self.piece_size
        raw >>= self.piece_size

        return raw

    def _is_valid(self, val):
        if type(val) is str:
            pieces = val.split(self.separator)
        elif type(val) is tuple:
            pieces = val
        else:
            return False

        if len(pieces) != self.pieces_amount:
            return False

        for i in pieces:
            if int(i, self.base) > 2**self.piece_size or int(i, self.base) < 0:
                return False

        return True

class IPv4AddrField(IPAddrField):
    """Address in IPv4 style.
    """
    separator = "."
    piece_size = 8
    pieces_amount = 4
    base = 10

class IPv6AddrField(IPAddrField):
    """Address in IPv6 style.
    """
    separator = ":"
    piece_size = 16
    pieces_amount = 8
    base = 16

class PaddingField(IntField):
    def _is_valid(self, val):
        if isinstance(val, int):
            return True
        return False

    def fillout(self):
        self._pre_fillout()

        if not self._value:
            self.bits = self._generate_value()
        else:
            self.bits = self._value
        return self._raw_value()
    
    def _raw_value(self):
        return 0

class Flags(Field):
    """Most of protocols have a special field with bit-flags.
    For those fields we use this subclass of Field.
    """

    def __init__(self, name, names, **preset):
        """Names has to be in correct order.
        If you use **preset, check if keys are in names list as well
        because of order issue.
        """
        super(Flags, self).__init__(name, bits=len(names))

        self._ordered_fields = names

        # initialize of self._value...
        # well we can call clear() to not duplicate the code
        self.clear()

        # if **preset exists then we update values
        for name in preset:
            if preset[name] == True:
                self.set(name)
            else:
                self.unset(name)

    def _is_valid(self, name):
        return self._value.has_key(name)

    def _set_bit(self, names, value):
        for flag_name in names:
            if self._is_valid(flag_name):
                self._value[flag_name].set(value)
            else:
                raise UMPAAttributeException, attr + ' not allowed'

    def clear(self):
        # we overwrite an attribute self._value
        # because we need a list instead of simple var here
        self._value = {}
        for flag in self._ordered_fields:
            self._value[flag] = BitField(flag)
        #self._value = dict.fromkeys(self._ordered_fields, False)
        self._modified = False

    def set(self, *names):
        self._set_bit(names, True)
        self._modified = True

    def unset(self, *names):
        self._set_bit(names, False)

    def get(self, *names):
        # we check if name of the field in the flag is correct
        result = [ self._value[val].get() for val in names
                                                    if self._is_valid(val) ]

        # if no results above we return whole list of values
        if len(result) < 1:
            result = self._value
        return result

    def _pre_fillout(self):
        pass

    def fillout(self):
        self._pre_fillout()

        raw = 0
        for bitname in self._ordered_fields:
            raw += self._value[bitname].fillout()
            raw <<= 1
        raw >>= 1
        return raw

class BitField(Field):
    bits = 1
    def __init__(self, name, value=None, auto=None):
        super(BitField, self).__init__(name, value, BitField.bits, auto)
        
        # we store value as a _default_view, it's necessary by generic
        # fillout, so for most of cases we don't need to make subclasses with
        # distinct fillout() method
        self._default_value = value
        if self._default_value:
            self.auto = True

    def _is_valid(self, val):
        # always True because it's bool type
        return True

    def get(self):
        return bool(self._value)

    def fillout(self):
        if self._value is None:
            self._value = self._generate_value()
            raw = self._raw_value()
            self.clear()
        else:
            raw = self._raw_value()

        return raw

    def _generate_value(self):
        """Generate value of bit.
        
        Be default it checks if self._default_value is defined,
        if so it returns this value.
        
        If you need more complex action,
        create subclass and overwrite this method.
        """
        if self._default_value:
            return bool(self._default_value)
        else:
            raise UMPAException, "value is not defined or _generate_value() \
                                                    method is not implemented."

    def _raw_value(self):
        if self._value:
            return 1
        else:
            return 0

class SpecialIntField(IntField):
    """Use this class if the field handle with other fields from the protocol
    or other layers/protocols.
    """
    def __init__(self, *args, **kwds):
        super(SpecialIntField, self).__init__(*args, **kwds)
        self.__temp_value = 0

    def get_tmpvalue(self):
        return self.__temp_value

    def set_tmpvalue(self, val):
        self.__temp_value = val

    def clear_tmpvalue(self):
        self.__temp_value = 0

    _tmp_value = property(get_tmpvalue, set_tmpvalue, clear_tmpvalue)

class Protocol(object):
    """Superclass for protocols.
    To implement new protocol, make a subclass.
    
    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """
    _ordered_fields = ()
    layer = None
    protocol_id = None

    def __init__(self, fields, **kw):
        super(Protocol, self).__setattr__('_fields', fields)

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
        kw.update(util.dict_from_sequence(args))

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

    def get_raw(self, protolol_container, protocol_bits):
        """Return raw bits of the protocol's object."""

        # The deal: we join all value's fields into one big number
        # (with taking care about amount of bits).
        # then we devide the number on byte-chunks
        # and pack it by struct.pack() function
        raw_value, bit = self._raw(protolol_container, protocol_bits)

        # protocol should return byte-compatible length
        if bit%BYTE != 0:
            raise UMPAException, 'odd number of bits in ' + self.__name__

        return raw_value, bit

    def _is_valid(self, field):
        """Overload it in subclasses."""
        raise NotImplementedError

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
