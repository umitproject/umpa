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
Generic Field classes.

Protocols' headers contain fields. Each field's objects should be an instance
of a Field class or of a subclass thereof (especially some generic subclasses
provided by this module).

Use these fields' classes to create new implementation of any protocols.
"""

import types

from umpa.utils.exceptions import UMPAException, UMPAAttributeException

class Field(object):
    """
    Superclass for any fields.

    Protocols' headers contain there fields.

    To implement new fields, create subclass of this class or any other
    common classes included in this module.

    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """

    bits = 0
    auto = False
    def __init__(self, name, value=None, bits=None, auto=None):
        """
        Create a new Field().

        @type name: C{str}
        @param name: name of the field.

        @type value: Optional
        @param value: predefined value of the field.

        @type bits: Optional C{int}
        @param bits: length of the field.

        @type auto: Optional C{bool}
        @param auto: information for users if the field can be auto-filling
        """

        self.name = name
        if auto is not None:
            self.auto = auto
        else:
            self.auto = self.__class__.auto

        if bits is not None:
            self.bits = bits
        if value is None:
            self._value = None
        # XXX hack for unitttests, normally Field is only super-class for others
        elif self.__class__ is Field:
            self._value = value
        else:
            self.set(value)

    def __str__(self):
        """
        Print in human-readable tree-style a content of the field.

        @return: the part of the whole tree which accords to the field.
        """

        if self.auto:
            return "| +-[ %-25s ]\t\t%s (auto - %s)" % (self.name,
                                        str(self._value), str(self.fillout()))
        else:
            return "| +-[ %-25s ]\t\t%s" % (self.name, str(self._value))

    def __repr__(self):
        """
        Print name of the Field
        """

        return self.name

    def get(self):
        """
        Return the current value of the field.

        Don't generate the value if the is not saved any but auto-filling
        is possible. In this case, just return None.

        @return: the current value of the field.
        """

        return self._value

    def set(self, value):
        """
        Set a value for the field.

        The new value is validing before assigment.

        @param value: new value for the field.
        """

        if self._is_valid(value):
            self._value = value
        else:
            raise UMPAAttributeException(str(value) + ' is not allowed')

    def clear(self):
        """
        Clear the current value of the field.
        """

        self._value = None

    def set_doc(self, text):
        """
        Set the pydocs of the field.

        It's important for new subclasses of the Field.
        Some GUIs use this information in hints etc.

        @type text: C{str}
        @param text: new pydoc for the field.
        """

        self.__doc__ = text

    def _is_valid(self, value):
        """
        Validate the new value.

        This method is an abstract. You HAVE TO override it.

        @param value: the new value

        @rtype: C{bool}
        @return: result of the validation.
        """

        raise NotImplementedError("this is abstract class")

    def _raw_value(self):
        """
        Convert the value to the raw mode.

        Raw value's type is a number. It has to be in big-endian order.
        The bits of the result of this method are inserted into the raw number
        of the whole protocol.

        This method is an abstract. You HAVE TO override it.
        You need to implement a conversion of the value here.
        E.g. for IntField is just return the value. But for some strings-fields
        you need to convert characters in the specific way.

        @rtype: C{number}
        @return: raw value of the field.
        """

        raise NotImplementedError("this is abstract class")

    def _generate_value(self):
        """
        Generate value for undefined yet field.

        This is auto-filling feature. If you implement this method, propably
        you should set the auto attribute to True for the class. It means that
        user doesn't need to set the value of the field.

        @return: auto-generated value of the field.
        """

        raise UMPAException("value is not defined or _generate_value()" 
                                                "method is not implemented.")

    def fillout(self):
        """
        Fillout the field.

        Generate the value if undefined and convert the result
        to the big-endian representation.

        @return: bits of the field for the (generated) value.
        """

        # we have to clear self._value if it was not defined
        # because of later usage
        if self._value is None:
            self._value = self._generate_value()
            raw = self._raw_value()
            self.clear()
        else:
            raw = self._raw_value()
        
        return raw

class IntField(Field):
    """
    Superclass for number-type fields.

    This class implemented _raw_value() and _is_valid() methods.
    You need to implement _generate_value() method if needed.

    IMPORTANT: You should overwrite this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """

    def _raw_value(self):
        """
        Convert the value to the raw mode.

        Raw value's type is a number. It has to be in big-endian order.
        The bits of the result of this method are inserted into the raw number
        of the whole protocol.
        
        For IntField there is nothing to convert. Just simple return the value.

        @rtype: C{number}
        @return: raw value of the field.
        """

        return self._value

    def _is_valid(self, value):
        """
        Validate if the value is not bigger than expected.

        @param value: the new value.

        @rtype: C{bool}
        @return: result of the validation.
        """

        if 2**self.bits > value:
            return True
        else:
            return False

class SpecialIntField(IntField):
    """
    This class is a specific one and has special meaning.
    
    It's a subclass of IntField.
    Use this class if the field handles with other fields from the protocol
    or other layers/protocols.

    E.g. Internet Header Length (IHL) field from the IP protocol needs to know
    some informations about others fields.

    Use _tmp_value attribute then in pre/post raw methods in protocol
    classes. Just assign to the _tmp_value needed information from other fields
    and implement _generate_value() method in the related way.
    Check umpa.protocols.IP module for examples.
    """

    def __init__(self, *args, **kwargs):
        """
        Create a new SpecialIntField().

        Call the super constructor and initiate temporary value.
        """

        super(SpecialIntField, self).__init__(*args, **kwargs)
        self.__temp_value = 0

    def get_tmpvalue(self):
        """
        Return temporary value.

        @rtype: C{int}
        @return: temporary value of the field.
        """

        return self.__temp_value

    def set_tmpvalue(self, value):
        """
        Set the temporary value.

        @type value: C{int}
        @param value: temporary value for special cases
        """

        self.__temp_value = value

    def clear_tmpvalue(self):
        """
        Clear the temporary value.
        """

        self.__temp_value = 0

    _tmp_value = property(get_tmpvalue, set_tmpvalue, clear_tmpvalue, """
    The temporary value -- attribute for special cases in pre/post raw methods.

    Use _tmp_value attribute in pre/post raw methods in protocol
    classes if you need handle with other fields.
    Assign to the _tmp_value needed information from other fields
    and implement _generate_value() method in the related way.
    Check umpa.protocols.IP module for examples.

    @type: C{int}
    """)

class EnumField(IntField):
    """
    This is a specific version of IntField and handles with enumerable fields.

    E.g. SMTP port is 25. To set/get value of port from TCP protocol,
    use "STMP" instead of "25". Read documentation for get() and set() methods
    for additional information.
    """

    enumerable = {}

    def get(self, human=False):
        """
        Return the current value of the field.

        @type human: Optional C{bool}
        @param human: if True, return human-readable value instead of numeric.
        (Default: False)
        """

        value = super(EnumField, self).get()
        if human:
            for k, val in self.enumerable.items():
                if val == value:
                    return k
        return value

    def set(self, value):
        """
        Set the new value of the field.

        Try to use value as a key for a dictionary ("SMTP" e.g.) and set
        the value returned by the dictionary.

        If value doesn't recognise as a dictionary key, try classic way.

        @type value: C{int} or C{str}
        @param value: assign new value in both ways (numeric and human).
        """
        
        # we try to use value as a "human" value
        # if doesn't work, then as a normal one
        try:
            super(EnumField, self).set(self.enumerable[value])
        except KeyError:
            super(EnumField, self).set(value)

class AddrField(Field):
    """
    Superclass for address-type fields.

    Subclasses of this class are related to the different kinds of addresses
    as IP addresses for example.
    """

    pass

class IPAddrField(AddrField):
    """
    Main class for IP-style adresses.

    Handle with 2 types of data:
     1. strings as "127.0.0.1" or "0:0:0:0:0:0:0:1"
     2. tuples as (127,0,0,1) or (0,0,0,0,0,0,0,1)
    """

    separator = ""
    base = 0
    piece_size = 0
    pieces_amount = 0
    bits = 0

    def set(self, value):
        """
        Set the new value of the field.
        
        @type value: C{str} or C{list} or C{tuple}
        @param value: new value for the field.
        """

        # convert list to tuple
        if isinstance(value, types.ListType):
            value = tuple(value)

        super(IPAddrField, self).set(value)

    def _raw_value(self):
        """
        Convert the value to the raw mode.

        Raw value's type is a number. It has to be in big-endian order.
        The bits of the result of this method are inserted into the raw number
        of the whole protocol.

        @rtype: C{number}
        @return: raw value of the field.
        """

        # convert the value to the list if it's str
        if isinstance(self._value, types.StringType):
            pieces = self._value.split(self.separator)
        else:
            pieces = self._value

        # add every piece of the address to the raw value
        # with bits-length of them keeping
        raw = 0
        for bit in pieces:
            bit = str(bit)
            raw += int(bit, self.base)
            raw <<= self.piece_size
        raw >>= self.piece_size

        return raw

    def _is_valid(self, value):
        """
        Validate the new value.

        Only str or tuple type of the value is allowed.

        @param value: the new value.

        @rtype: C{bool}
        @return: result of the validation.
        """

        if isinstance(value, types.StringType):
            pieces = value.split(self.separator)
        elif isinstance(value, types.TupleType):
            pieces = value
        else:
            return False

        if len(pieces) != self.pieces_amount:
            return False

        for i in pieces:
            i = str(i)
            try:
                i_base = int(i, self.base)
            except ValueError:
                return False
            if i_base >= 2**self.piece_size or i_base < 0:
                return False

        return True

class IPv4AddrField(IPAddrField):
    """
    Address in IPv4 style.

    Handle with 2 types of data:
     1. strings as "127.0.0.1"
     2. tuples as (127,0,0,1)
    """

    separator = "."
    piece_size = 8
    pieces_amount = 4
    base = 10
    bits = 32

#class IPv6AddrField(IPAddrField):
#    """
#    Address in IPv6 style.
#
#    Handle with 2 types of data:
#     1. strings as "0:0:0:0:0:0:0:1"
#     2. tuples as (0,0,0,0,0,0,0,1)
#
#    @note: This field is really limited and you can't use address
#    like 2001:db8::1428:57ab. All groups have to be pass.
#    This issue should be fixed soon.
#    """
#
#    separator = ":"
#    piece_size = 16
#    pieces_amount = 8
#    base = 16
#    bits = 128

class PaddingField(SpecialIntField):
    """
    This class is for padding cases.

    PaddingField is used to ensure that the header ends on a 32 bit boundary.
    This is common fields for many protocols.
    """

    bits = 0
    auto = True

    def __init__(self, name, word=32, *args, **kwargs):
        """
        Create a new PaddingField().

        @type word: C{int}
        @param word: length of field which need padding (default: 32)
        
        Call the super constructor and initiate extra attributes.

        Please note that padding is always done by using zeros (0).
        """

        self._word = word
        super(PaddingField, self).__init__(name, 0, *args, **kwargs)

    def fillout(self):
        """
        Fillout the field.

        If undefined value, set the correct length of the field and generate
        a value.

        @return: call _raw_value() method for conversion.
        """

        if not self.get():
            self.bits = self._generate_value()
        else:
            self.bits = self.get()
        return self._raw_value()
    
    def _is_valid(self, value):
        """
        Validate if the value is not bigger than expected.

        @param value: the new value.

        @rtype: C{bool}
        @return: result of the validation.
        """

        if isinstance(value, types.IntType) and 0 <= value <= self._word:
            return True
        return False

    def _raw_value(self):
        """
        Don't convert the value. Return 0.

        Padding B{always} contains bits with 0 assigned.

        @rtype: C{int}
        @return: 0
        """

        return 0

    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return (self._word - (self._tmp_value % self._word)) % self._word

class Flags(Field):
    """
    This is special case of field - Flags.

    Most of protocols have a special field with bit-flags.
    E.g. TCP use them for ACK,SYN and others flags.
    """

    def __init__(self, name, names, **preset):
        """
        Create a new Flags()

        List names need to be in correct order. List contains string names
        of the bit-flags.

        @type name: C{str}
        @param name: name of the field.
        
        @type names: C{list}
        @param names: list of bit-flags (C{str} type) B{in correct order}.

        @type preset: C{bool}
        @param preset: predefined values of bit-flags (defailt: I{0})
        """
        super(Flags, self).__init__(name, bits=len(names))

        self._ordered_fields = names

        # initialize of self._value...
        # call clear() to not duplicate the code
        self.clear()

        # if **preset exists then we update values
        for name in preset:
            if preset[name] is True:
                self.set(name)
            else:
                self.unset(name)

    def __str__(self):
        """
        Print in human-readable tree-style a content of the field.

        Call print statement for bit-flags.

        @return: the part of the whole tree which accords to the field.
        """

        print "| +-[ %-25s ]" % self.name
        print "| | \\"
        for bit in self._ordered_fields:
            print self._value[bit]
        print "| | /"
        return "| \\-[ %-25s ]\t\tcontains %d bit flags" % (self.name,
                                                    len(self._ordered_fields))

    def get(self, *names):
        """
        Return list of passed bits values.

        If no names passed or no results, return the whole list with values
        of every flag-bits.

        @type names: C{str}
        @param names: names of bit-flags.

        @return: list of passed bits values.
        """

        for bit in names:
            if not self._is_valid(bit):
                raise UMPAAttributeException('no bit named ' + bit)

        result = [ self._value[val].get() for val in names ]

        # if no results above return whole list of values
        if len(result) < 1:
            result = [ self._value[bit].get() for bit in self._ordered_fields ]
        return result


    def set(self, *names):
        """
        Set logical True for passed bit-flags.

        @type names: C{str}
        @param names: names of bit-flags.
        """

        self._set_bit(names, True)

    def unset(self, *names):
        """
        Set logical False for passed bit-flags.

        @type names: C{str}
        @param names: names of bit-flags.
        """

        self._set_bit(names, False)

    def clear(self):
        """
        Clear the values of bit-flags.

        Re-create a storing dictionary.
        """

        # we overwrite an attribute self._value
        # because we need a list instead of simple var here
        self._value = {}
        for flag in self._ordered_fields:
            self._value[flag] = BitField(flag, False)

    def fillout(self):
        """
        Fillout the field.

        Call fillout() methods for every bit-flags.
        Return concatenated result.

        @return: bits of the bit-flags.
        """

        raw = 0
        for bitname in self._ordered_fields:
            raw += self._value[bitname].fillout()
            raw <<= 1
        raw >>= 1
        return raw

    def _is_valid(self, name):
        """
        Validate if the value is not bigger than expected.

        @param name: the name of the bit-flag.

        @rtype: C{bool}
        @return: result of the validation.
        """

        return name in self._value

    def _set_bit(self, names, value):
        """
        Set the value for a bit.

        Set True or False for the bit-flag.
        Set the same value for every bit-flags from the list.

        @type names: C{list}
        @param names: list of names to set the value

        @type value: C{bool}
        @param value: the logical value.
        """

        for flag_name in names:
            if self._is_valid(flag_name):
                self._value[flag_name].set(value)
            else:
                raise UMPAAttributeException(flag_name + ' is not allowed')

class BitField(Field):
    """
    This class is used for bit-flags of Flags field.

    Flags is a field which contains several independent bits.
    Each of the bits is an instance of BitField.
    """

    bits = 1
    auto = False

    def __str__(self):
        """
        Print in human-readable tree-style a content of the field.

        @return: the part of the whole tree which accords to the field.
        """

        return "| |  -{ %-23s }\t\t%d" % (self.name, int(bool(self._value)))

    def get(self):
        """
        Return the current value of the field.

        @return: the current value of the field.
        """

        if self._value is None:
            return self._value
        return bool(self._value)

    def fillout(self):
        """
        Fillout the field.

        Generate the value if undefined and convert the result
        to the big-endian representation.

        @return: bits of the field for the (generated) value.
        """

        if self._value is None:
            self._value = self._generate_value()
            raw = self._raw_value()
            self.clear()
        else:
            raw = self._raw_value()

        return raw

    def _is_valid(self, value):
        """
        Validate the new value.

        @param value: the new value

        @rtype: C{bool}
        @return: C{True}, becuase this is a bool type so every value is correct.
        """

        # always True because it's bool type
        return True

    def _raw_value(self):
        """
        Convert the value to the raw mode.

        In this case simple return 0 or 1.

        @rtype: C{number}
        @return: raw value of the field.
        """

        return int(bool(self.get()))
