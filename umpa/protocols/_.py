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

    def set(self, value):
        if self._is_valid(value):
            self._value = value
        else:
            raise UMPAAttributeException, value + ' not allowed'

    def get(self):
        return self._value

    def clear(self):
        self._value = None

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

    def fillout(self):
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

class IPv4Field(AddrField):
    """Address in IPv4 style.
    """
    def _is_valid(self, val):
        """Return True if passed value is correct for IPv4.
        """
        bytes = val.split(".")

        if len(bytes) != 4:
            return False

        for i in bytes:
            if int(i) > 255 or int(i) < 0:
                return False

        return True

    def _raw_value(self):
        """Convert IPv4 address (string) to binary value.
        """
        bytes = self._value.split(".")

        raw = 0
        for b in bytes:
            raw += int(b)
            raw <<= 8
        raw >>= 8

        return raw

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
        # we overwrite an attribute self._value
        # because we need a list instead of simple var here
        self._value = {}
        for flag in self._ordered_fields:
            self._value[flag] = BitField(flag)
        #self._value = dict.fromkeys(self._ordered_fields, False)

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

    def set(self, *names):
        self._set_bit(names, True)

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

class Protocol(object):
    """Superclass for protocols.
    To implement new protocol, make a subclass.
    
    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """
    _ordered_fields = ()
    layer = None

    def __init__(self, fields, **kw):
        #self._fields = {}
        super(Protocol, self).__setattr__('_fields', fields)

    def __setattr__(self, attr, val):
        """Set value of the field."""

        # we can do the same without _is_valid() with just try/except section
        # but Francesco asked me about this method
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

    def _get_flag_obj(self):
        """Check if the protocol has special field 'Flags'
         and return it.
         """
        # XXX: what if there is more than one Flags field in the protocol?
        flag_field = None
        for obj in self._fields:
            if type(obj) == Flags:
                flag_field = obj
                break
        return flag_field

    def set_flags(self, *args, **kw):
        """Set flags with dict using.

        There are 2 ways to do that with using tuple or dict-style.

        There is no effect if the protocol doesn't have this field.
        """

        # converting args list to the dict and update our kwargs
        kw.update(util.dict_from_sequence(args))

        flag_field = _get_flag_obj()
        if flag_field is not None:
            for flag_name in kw:
                if kw[flag_name] == True:
                    flag_field.set(flag_name)
                elif kw[flag_name] == False:
                    flag_field.unset(flag_name)
                else:
                    raise UMPAException, "Only bool type is supported" 
        else:
            raise UMPAAttributeException, 'No Flags instance for this protocol'

    def get_flags(self, *args):
        flag_field = _get_flag_obj()
        if flag_field is not None:
            return flag_field.get(*args)
        else:
            return None

    def get_raw(self):
        """Return raw bits of the protocol's object."""

        # The deal: we join all value's fields into one big number
        # (with taking care about amount of bits).
        # then we devide the number on byte-chunks
        # and pack it by struct.pack() function
        bit = 0
        raw_value = 0
        # lets make a biiiig number ;)
        for field in reversed(self._ordered_fields):
            raw_value |= self._get_field(field).fillout() << bit
            bit += self._get_field(field).bits
        
        # protocol should return byte-compatible length
        if bit%BYTE != 0:
            raise UMPAException, 'odd number of bits in ' + self.__name__

        # check how many bytes we need
        bytes = bit/BYTE
        # split the number on byte-chunks
        l = [ (raw_value & (0xff << (BYTE*i))) >> BYTE*i
                                    for i in reversed(xrange(bytes)) ]
        # and pack it
        header_pack = struct.pack('!' + 'B'*bytes, *l)
        return header_pack

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
