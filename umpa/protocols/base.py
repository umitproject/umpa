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

from umpa import utils

class Field(object):
    def __init__(self, bits, auto=False):
        """Set auto if you wish to take care about the field
        by the library. Then you will have to write how
        to manage the field.
        """
        self._bits = bits
        self._auto = auto
        self._value = None   # default value of the field

    def set(self, value):
        if self.is_valid(value):
            self.value = value

    def get(self):
        return self.value

    def is_valid(self, val):
        """Should be overload by sub-classes.

        Otherwise always return true.
        """
        return True

class Flags(Field):
    """Most of protocols have a special field with bit-flags.
    For those fields we use this subclass of Field.
    """

    def __init__(self, auto=False, *names):
        Field.__init__(self, len(names), auto)

        # we overwrite an attribute self._value
        # because we need a list instead of simple var here
        self._value = []
        self.valid_fields = list(names)

    def is_valid(self, val):
        if val in self.valid_fields:
            return True
        else:
            return False

    def set(self, kw):
        for flag_name in kw:
            if self.is_valid(self, flag_name):
                utils.get_item_by_name(self._value, self.valid_fields,
                                                    flag_name) = kw[flag_name]

    def get(self, *names):
        # we check if name of the field in the flag is correct
        result = [ utils.get_item_by_name(self._value, self.valid_fields, val)
                for val in names if val in self.valid_fields ]
        # if no results above we return whole list of values
        if len(result) < 1:
            result = self._value
        return result

class Protocol(object):
    def __init__(self, **kw):
        # TODO
        # ok, there is an ugly implementation of this.
        # because there isn't ordered dict type.
        # so the fact is, that we use 2 lists
        # first with objects (fields)
        # and second with valid names of objects

        # there is some implementation in PEP372
        # and it should be implemtented

        # also there is other wrong now, because this mechanism isn't
        # only this class but also in sub-classes
        # it means that it spreads out and also means about bad API design
        self._fields = []
    # XXX chyba trzeba dodac jakies get flags czy cos
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

    def set_flags(self, *args, **kw):
        """Set flags with dict using.

        There are 2 ways to do that with using tuple or dict-style.

        There is no effect if the protocol doesn't have this field.
        """

        # converting args list to the dict and update our kwargs
        kw.update(util.dict_from_sequence(args))

        # first checking if the protocol has special field 'Flags'
        # and assign it to a local variable
        # XXX: what if there is more than one Flags field in the protocol?
        for obj in self._fields:
            if type(obj) == Flags:
                flag_field = obj
                break

        if flag_field is not None:
            flag_field.set(kw)

    def get_raw(self):
        """Return raw bit of the protocol's object"""
        print "Not implemented yet."
        return False

    def _is_valid(self, field):
        """Overload it in subclasses."""
        raise NotImplementedError

    #def set_flags(self, val):
    #    pass
    #def get_flags(self):
    #    return self._Flags
    #flags = property(get_flags, set_flags)

class Layer4(Protocol):
    pass
