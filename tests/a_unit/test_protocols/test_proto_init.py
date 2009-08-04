#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
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

import os
import umit.umpa.protocols

class TestProtocolInit(object):
    def test_import_global_protos(self):
        assert umit.umpa.protocols.Ethernet
        assert umit.umpa.protocols.SLL
        assert umit.umpa.protocols.IP
        assert umit.umpa.protocols.UDP
        assert umit.umpa.protocols.TCP
        assert umit.umpa.protocols.Payload

    def test_get_locals(self):
        for file in os.listdir(os.path.join(os.path.expanduser('~'),
                            '.umpa', 'umpa_plugins', 'protocols')):
            if file.startswith('_'):
                continue
            assert file[:-3] in umit.umpa.protocols.get_locals().keys()

    def test_import_local_protos(self):
        for file in os.listdir(os.path.join(os.path.expanduser('~'),
                            '.umpa', 'umpa_plugins', 'protocols')):
            if file.startswith('_'):
                continue
            assert getattr(umit.umpa.protocols, file[:-3])
