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
Protocol - super-class for protocols implemenations.

Every protocols have to be subclassed from the Protocol.
Some methods have to be overridden. Read Protocol's docstrings for more
information.
"""

from umit.umpa.protocols._consts import BYTE
from umit.umpa.protocols._fields import Field, Flags
from umit.umpa.utils.exceptions import UMPAException, UMPAAttributeException
from umit.umpa.utils.tools import dict_from_sequence as _dict_from_sequence

class Protocol(object):
    """
    Superclass for every protocol's implementations.
   
    You have to override following methods:
     - _pre_raw()
     - _post_raw()
    They are used to make some tasks especially with SuperIntField objects.
    Check IP.py, TCP.py for examples.

    Also, override this __doc__ to get hints in some frontends
    like the one provided by Umit Project.
    """

    _ordered_fields = ()
    layer = None
    protocol_id = None
    name = None

    def __init__(self, fields_list, **preset):
        """
        Create a new Protocol().

        @type fields_list: C{list}
        @param fields_list: list of fields B{in correct order}.

        @param preset: predefined values for fields.
        """

        # pack objects of header's fields to the dict
        fields = dict(zip(self._ordered_fields, fields_list))

        # because of overwritten __setattr__ we need to assign with __dict__
        self.__dict__['_fields'] = fields
        self.__dict__['payload'] = None
        self.__dict__['__raw_value'] = None

        # setting up passed fields
        for field in preset:
            setattr(self, field, preset[field])

        # short-fieldname update
        for field in fields:
            self.get_field(field)._shortname = field

    def __getattr__(self, attr):
        """
        Return the value of the field.
        
        @type attr: C{str}
        @param attr: name of the field.

        @return: value of the field.
        """
        
        return self.get_field(attr).get()

    def __setattr__(self, attr, value):
        """
        Set value of the field.

        @type attr: C{str}
        @param attr: name of the field.

        @param value: the new value.
        """

        self.get_field(attr).set(value)

    def __str__(self):
        """
        Print in human-readable tree-style a content of the protocol.

        Call print statement for fields.

        @return: the part of the whole tree which accords to the protocol.
        """

        print "+-< %-27s >" % self.name
        print "| \\"
        for field in self.get_fields():
            print field
        print "\\-< %-27s >\tcontains %d fields" % (self.name,
                                                            len(self._fields))
        return super(Protocol, self).__str__()

    def _is_valid(self, field):
        """
        Validate if the filed is allowed.

        @param field: requested field.

        @rtype: C{bool}
        @return: result of the validation.
        """

        return field in self._fields

    @classmethod
    def get_fields_keys(cls):
        """
        Yield the ordered sequence of the fields' names.

        This is a generator for ordered names (keys) of header's fields.
        """

        for field in cls._ordered_fields:
            yield field

    def get_fields(self):
        """
        Yield the ordered sequence of the fields.

        This is a generator for ordered fields.
        """
        
        for field in self._ordered_fields:
            yield self.get_field(field)
    
    def get_field(self, keyname):
        """
        Return the field.

        @type keyname: C{str}
        @param keyname: name of the field

        @rtype: C{Field}
        @return: requested field.
        """

        if self._is_valid(keyname):
            return self._fields[keyname]
        else:
            raise UMPAAttributeException(keyname + ' is not allowed')

    def set_fields(self, *args, **kwargs):
        """
        Set fields of the protocol.

        There are 2 ways to do that with using tuple or dict-style.
        For tuple, use sequence as: field_name1, value1, field_name2, value2.
        For dict, use dict ;) field_name1=value1, field_name2=value2.

        @param args: sequence of field_name and value.

        @param kwargs: field_name=value.
        """
        
        if len(args) % 2:
            raise UMPAAttributeException('wrong amount of passed arguments')
        # converting args list to the dict and update our kwargs
        kwargs.update(_dict_from_sequence(args))

        # first check if all keys are valid to avoid partial-changing
        for key in kwargs:
            if not self._is_valid(key):
                raise UMPAAttributeException(key + ' is not allowed; '
                                            'nothing has changed')

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_flags(self, name, *args):
        """
        Return flags of the field.

        @type name: C{str}
        @param name: name of the field.

        @param args: names of flags.

        @rtype: C{list}
        @return: list of flags.
        """

        flag_field = self.get_field(name)
        if not isinstance(flag_field, Flags):
            raise UMPAAttributeException("No Flags instance for " + name)

        if not args:
            return flag_field.get([])
        return flag_field.get(*args)

    def set_flags(self, name, *args, **kwargs):
        """
        Set flags for flags-field.

        There are 2 ways to do that with using tuple or dict-style.
        For tuple, use sequence as: flag_name1, value1, flag_name2, value2.
        For dict, use dict ;) flag_name1=value1, flag_name2=value2.

        @type name: C{str}
        @param name: name of the field.

        @param args: sequence of field_name and value.

        @param kwargs: field_name=value.
        """

        if len(args) % 2:
            raise UMPAAttributeException('wrong amount of passed arguments')
        # converting args list to the dict and update our kwargs
        kwargs.update(_dict_from_sequence(args))

        flag_field = self.get_field(name)
        if isinstance(flag_field, Flags):
            for flag_name in kwargs:
                if kwargs[flag_name]:
                    flag_field.set(flag_name)
                else:
                    flag_field.set(False, flag_name)
        else:
            raise UMPAAttributeException("No Flags instance for " + name)

    def get_offset(self, field):
        """
        Return the offset for the field.

        This offset is for the current protocol, not the packet.

        @type field: C{str} or C{Field}
        @param field: name of the field

        @rtype: C{int}
        @return: offset of the field in bits.
        """

        # checking if argument is a key or instance
        if isinstance(field, str):
            field_list = self._ordered_fields
        elif isinstance(field, Field):
            field_list = [ f for f in self.get_fields() ]
        else:
            raise UMPAException(str(type(field)) + ' unsupported')
    
        if field not in field_list:
            raise UMPAAttributeException(repr(field) + ' is not allowed')

        offset = 0
        for i, val in enumerate(field_list):
            if field == val:
                break
            offset += self.get_field(self._ordered_fields[i]).bits
        return offset

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        Some fields (especially SpecialIntField) need to handle with other
        fields. Do it here. If they need to handle with other fields B{after}
        the fillout() (e.g. to calculate a checksum), use _post_raw() instead.

        I{Currently} means that if we're generating raw values for
        the packet/protocol it's done by some loops. So, currently it's
        the value in the current stage of that loops.

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
        
        raise NotImplementedError("this is abstract class")

    def _raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Call pre/post handling with other fields and merge results of fillout.

        Call fillout() method for every fields from the protocol.
        Handle with fields by pre/port methods.

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

        # because of some protocols implementation, there are some tasks before
        # we call fillout() for fields
        raw_value, bit = self._pre_raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        # so we make a big number with bits of every fields of the protocol
        for field in reversed(self._ordered_fields):
            field_bits = self.get_field(field).fillout()
            raw_value |= field_bits << bit
            bit += self.get_field(field).bits

        # because of some protocols implementation, there are some tasks after
        # we call fillout() for fields
        raw_value, bit = self._post_raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields after calling fillout() for them.

        Some fields (especially SpecialIntField) need to handle with other
        fields. First, think to do it in _pre_raw() method. But if they need
        to handle with other fields B{after} the fillout() (e.g. to calculate
        a checksum), do it here.

        I{Currently} means that if we're generating raw values for
        the packet/protocol it's done by some loops. So, currently it's
        the value in the current stage of that loops.

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
        
        raise NotImplementedError("this is abstract class")

    def get_raw(self, protocol_container, protocol_bits):
        """
        Return raw bits of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        raw_value = 0
        bit = 0
        # The deal: we join all value's fields into one big number
        # (with taking care about amount of bits).
        # then we devide the number on byte-chunks
        # and pack it by struct.pack() function
        raw_value, bit = self._raw(raw_value, bit, protocol_container,
                                                                protocol_bits)

        # protocol should return byte-compatible length
        if bit % BYTE != 0:
            raise UMPAException('odd number of bits in ' + str(self.name))

        self.__dict__['__raw_value'] = raw_value
        return raw_value, bit

    def load_raw(self, buffer):
        """
        Load raw and update a protocol's fields.

        @return: raw payload
        """

        raise UMPAException("protocol doesn't support decoding "
                            "or an abstract class.")
