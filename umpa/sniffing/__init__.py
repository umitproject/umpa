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

import os.path

import umpa
from umpa.utils.exceptions import UMPASniffingException

if umpa.config['libpcap']:
    modulepath = "umpa.sniffing.libpcap.%s" % umpa.config['libpcap']
    try:
        lpcap = __import__(modulepath, fromlist=[None])
    except ImportError, err:
        raise UMPASniffingException("unknown libpcap's wrapper.\n" + str(err))
    lpcap._backend = umpa.config['libpcap']
    del modulepath
else:
    raise UMPASniffingException("unknown/missing libpcap's wrapper")

def get_available_devices():
    """
    Return list of network devices.

    These devices are suitable for packets capturing.

    @note: There may be network devices that cannot be used for capturing
    because e.g. that process might not have sufficient privileges.
    
    @return: list of network devices
    """

    return lpcap.findalldevs()

def sniff(count, filter=None, device=None, timeout=0, snaplen=1024,
                                                        promisc=True):
    """
    Sniff packets and return list of them.

    @type count: C{int}
    @param count: number of sniffing packets

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type device: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing
    """

    session = lpcap.open_pcap(device, snaplen, promisc, timeout)
    if filter:
        session.setfilter(filter)
    captured = []
    for i in xrange(count):
        captured.append(session.next())
    return captured

def sniff_next(filter=None, device=None, timeout=0, snaplen=1024,promisc=True):
    """
    Sniff one packet and return it.

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type device: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing
    """
    return sniff(1, filter, device, timeout, snaplen, promisc)[0]

def sniff_loop(count=0, filter=None, device=None, timeout=0, snaplen=1024,
                            promisc=True, callback=None, callback_args=None):
    """
    Sniff packets and call a callback function for each.

    @type count: C{int}
    @param count: number of sniffing packets; 0 means infinity (default: I{0})

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type device: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing

    @type callback: C{func}
    @param callback: function with (timestamp, pkt, *callback_args) prototype

    @type callback_args: C{list}
    @param callback_args: additional arguments for callback function
    """

    if callback_args is None:
        callback_args = []

    session = lpcap.open_pcap(device, snaplen, promisc, timeout)
    if filter:
        session.setfilter(filter)
    session.loop(count, callback, *callback_args)

def sniff_any():
    """
    Sniff any first upcoming packet and return it.
    """

    return sniff(1, device='any')

def from_file(filename, count=0, filter=None):
    """
    Load data from pcap file instead of sniffing online.

    Call callback for each or return list of packets.

    @type filename: C{str}
    @param filename: path to a file in pcap format

    @type count: C{int}
    @param count: number of sniffing packets; 0 means infinity (default: I{0})

    @type filter: C{str}
    @param filter: BPF filter
    """

    if os.path.isfile(filename):
        f = lpcap.open_pcap(filename)
    else:
        raise UMPASniffingException("can't open file: %s" % filename)

    if filter:
        f.setfilter(filter)
    if count > 0:
        packets = []
        for i in xrange(count):
            packets.append(f.next())
    else:
        packets = f.readpkts()

    return packets

def from_file_loop(filename, count=0, filter=None, callback=None,
                                                callback_args=None):
    """
    Load data from pcap file instead of sniffing online.

    Call callback for each or return list of packets.

    @type filename: C{str}
    @param filename: path to a file in pcap format

    @type count: C{int}
    @param count: number of sniffing packets; 0 means infinity (default: I{0})

    @type filter: C{str}
    @param filter: BPF filter

    @type callback: C{func}
    @param callback: function with (timestamp, pkt, *callback_args) prototype

    @type callback_args: C{list}
    @param callback_args: additional arguments for callback function
    """

    if callback_args is None:
        callback_args = []

    if os.path.isfile(filename):
        f = lpcap.open_pcap(filename)
    else:
        raise UMPASniffingException("can't open file: %s" % filename)

    if filter:
        f.setfilter(filter)
    f.loop(count, callback, *callback_args)

def to_file():
    pass
