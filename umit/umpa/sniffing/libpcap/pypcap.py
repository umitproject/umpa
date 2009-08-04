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

import pcap

from umit.umpa.sniffing.libpcap._abstract import *
from umit.umpa.utils.exceptions import UMPASniffingException

# see umit.umpa.sniffing.libpcap._abstract for docstrings

def lookupdev():
    try:
        result = pcap.lookupdev()
    except OSError, msg:
        raise UMPASniffingException(msg)
    return result

def findalldevs():
    try:
        result = pcap.findalldevs()
    except OSError, msg:
        raise UMPASniffingException(msg)
    return result

class open_pcap(open_pcap):
    def __init__(self, device=None, snaplen=1024, promisc=True, to_ms=0):
        if device is None:
            self.device = lookupdev()
        else:
            self.device = device
        self.snaplen = snaplen
        self.promisc = promisc
        self.to_ms = to_ms

        try:
            self._pcap = pcap.pcap(self.device, self.snaplen, self.promisc,
                                                                self.to_ms)
        except OSError, msg:
            raise UMPASniffingException(msg)

    def __iter__(self):
        return self

    def dispatch(self, cnt, callback, *user):
        return self._pcap.dispatch(cnt, callback, *user)

    def loop(self, cnt, callback, *user):
        return self._pcap.loop(cnt, callback, *user)

    def next(self):
        return self._pcap.next()

    def setfilter(self, filter):
        self._pcap.setfilter(filter)

    def datalink(self):
        return self._pcap.datalink()

class dumper(dumper):
    def __init__(self, p=None, fname=None, open=True):
        if p is not None:
            # XXX dirty hack
            # the next line has a dirty hack and looks like some design problems
            # feel free to propose better solution or send a patch
            #
            # anyway, Joao Medeiros proposed to put a quote here:
            # "In Python, there isn't much of an idea of "Private"
            # Python's philosophy is "We're all consenting adults here."
            # Thus, there isn't much of an idea of "friends" either.
            # In Java terminology, on a technical level everybody is already 
            # friends with everybody else already." by Jeremy Bowers
            self._pcap = p._pcap
        else:
            self._pcap = None
        self.fname = fname
        self._dump = pcap.dump(self._pcap, self.fname, open)

    def open(self, p=None, fname=None):
        if p is not None:
            # XXX dirty hack - same as above
            self._pcap = p._pcap
        if fname is not None:
            self.fname = fname

        try:
            self._dump.open(self._pcap, self.fname)
        except OSError, msg:
            raise UMPASniffingException(msg)

    def dump(self):
        if not self._dump:
            raise UMPASniffingException("not dump file is opened."
                                        "use open() first.")
        self._dump.dump()

    def flush(self):
        if not self._dump:
            raise UMPASniffingException("not dump file is opened."
                                        "use open() first.")
        self._dump.flush()

    def close(self):
        if not self._dump:
            raise UMPASniffingException("not dump file is opened."
                                        "use open() first.")
        self._dump.close()
