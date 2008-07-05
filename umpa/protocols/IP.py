#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Adriano Monteiro Marques.
#
# Author: Bartosz SKOWRON <getxsick at gmail dot com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import base

class IP(base.Protocol):
    def __init__(self, **kw):
        # attributes listed below shouldn't be modifed by user
        # they will be generated automatically
        self._version = None
        self._ihl = None
        self._total_length = None
        self._fragment_offset = None
        self._header_checksum = None
        self._padding = None

        # setting up passed fields
        for field in kw:
            setattr(self, field, kw[field])

    # fields

    def set_type_of_service(self, val):
        pass
    def get_type_of_service(self):
        return self._type_of_service
    type_of_service = property(get_type_of_service, set_type_of_service)

    def set_identification(self, val):
        pass
    def get_identification(self):
        return self._identification
    identification = property(get_identification, set_identification)

    def set_time_to_live(self, val):
        pass
    def get_time_to_live(self):
        return self._time_to_live
    time_to_live = property(get_time_to_live, set_time_to_live)

    def set_protocol(self, val):
        pass
    def get_protocol(self):
        return self._protocol
    protocol = property(get_protocol, set_protocol)

    def set_source_address(self, val):
        pass
    def get_source_address(self):
        return self._source_address
    source_address = property(get_source_address, set_source_address)

    def set_destination_address(self, val):
        pass
    def get_destination_address(self):
        return self._destination_address
    destination_address = property(get_destination_address,
            set_destination_address)

    def set_option(self, val):
        pass
    def get_option(self):
        return self._option
    option = property(get_option, set_option)
