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

def findalldevs():
    """
    Return list of network devices.

    These devices can be opened with open_live().

    @note: There may be network devices that cannot be opened
    with open_live() by process calling findalldevs(), because
    e.g. that process might not have sufficent priviliges to open them
    for capturing
    
    @return: list of network devices
    """

    raise NotImplementedError("not implemented method for the "
                    "selected libpcap backend or abstract module")

def lookupdev():
    """
    Return the name of the first network device that is suitable for
    packet capture

    @return: name of the device
    """

    raise NotImplementedError("not implemented method for the "
                    "selected libpcap backend or abstract module")

def open_offline(fname):
    """
    Open a file in tcpdump format for reading.
    """

    raise NotImplementedError("not implemented method for the "
                    "selected libpcap backend or abstract module")

class open_live(object):
    """
    Packet capture descriptor.
    """

    def __init__(self, device=None, snaplen=1024, promisc=True, to_ms=0):
        """
        @type device: C{str}
        @param device: network device for capturing;
                       if None try to use "any" if suitable or first found.

        @type snaplen: C{int}
        @param snaplen: maximum number of bytes to capture

        @type promisc: C{bool}
        @param promisc: set promiscuous mode

        @type to_ms: C{int}
        @param to_ms: read timeout in miliseconds
        """

        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")

    def dispatch(self, cnt, callback, *user):
        """
        Collect and process packets. Return if cnt or to_ms
        (see the constructur param) is occured.

        @type cnt: C{int}
        @param cnt: maximum number of packets to process before returning

        @type callback: C{func}
        @param callback: function to be called for captured packets

        @param user: additional arguments for callback functions
        """

        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")

    def loop(self, cnt, callback, *user):
        """
        Collect and process packets. Return if cnt is occured.

        @type cnt: C{int}
        @param cnt: maximum number of packets to process before returning

        @type callback: C{func}
        @param callback: function to be called for captured packets

        @param user: additional arguments for callback functions
        """
        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")

    def next(self):
        """
        Collect and return the first captured packet.

        @return: captured packet.
        """

        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")

    def setfilter(self, filter):
        """
        Specify a filter.

        If compiling it's needed, it's done also.

        @type filter: C{str}
        @param filter: filter string in BPF format (see pcap manual)
        """

        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")

    def dump_open(self):
        raise NotImplementedError("not implemented method for the "
                        "selected libpcap backend or abstract module")
