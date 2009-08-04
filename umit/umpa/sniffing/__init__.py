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

import umit.umpa
from umit.umpa.protocols._decoder import decode
from umit.umpa.utils.exceptions import UMPASniffingException

if umit.umpa.config['libpcap']:
    modulepath = "umit.umpa.sniffing.libpcap.%s" % umit.umpa.config['libpcap']
    try:
        lpcap = __import__(modulepath, fromlist=[None])
    except ImportError, err:
        raise UMPASniffingException("unknown libpcap's wrapper.\n" + str(err))
    lpcap._backend = umit.umpa.config['libpcap']
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
                                            promisc=True, dump=None):
    """
    Sniff packets and return list of them.

    @type count: C{int}
    @param count: number of sniffing packets

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type timeout: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing

    @type dump: C{str}
    @param dump: path to file where store the result
    """

    session = lpcap.open_pcap(device, snaplen, promisc, timeout)
    if filter:
        session.setfilter(filter)
    d = None
    if dump is not None:
        d = lpcap.dumper(session, dump)
    captured = []
    for i in xrange(count):
        p = decode(session.next()[1], session.datalink())
        captured.append(p)
        if d is not None:
            d.dump()
    if d is not None:
        d.flush()
    return captured

def sniff_next(filter=None, device=None, timeout=0, snaplen=1024,promisc=True,
                                                                    dump=None):
    """
    Sniff one packet and return it.

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type timeout: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing

    @type dump: C{str}
    @param dump: path to file where store the result
    """
    return sniff(1, filter, device, timeout, snaplen, promisc, dump)[0]

def sniff_loop(count=0, filter=None, device=None, timeout=0, snaplen=1024,
                promisc=True, dump=None, callback=None, callback_args=None):
    """
    Sniff packets and call a callback function for each.
    
    @type count: C{int}
    @param count: number of sniffing packets; 0 means infinity (default: I{0})

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type timeout: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing

    @type dump: C{str}
    @param dump: path to file where store the result

    @type callback: C{func}
    @param callback: function with (timestamp, pkt, *callback_args) prototype

    @type callback_args: C{list}
    @param callback_args: additional arguments for callback function
    """
    
    if callback is None:
        raise UMPASniffingException("no callback function is passed.")

    if callback_args is None:
        callback_args = []

    session = lpcap.open_pcap(device, snaplen, promisc, timeout)
    if filter:
        session.setfilter(filter)
    d = None
    if dump is not None:
        d = lpcap.dumper(session, dump)

    i = 0
    while 1:
        if i == count and count > 0:
            break
        ts, pkt = session.next()
        decoded_pkt = decode(pkt, session.datalink())
        if d is not None:
            d.dump()
        callback(ts, decoded_pkt, *callback_args)
        i += 1
    if d is not None:
        d.flush()

def sniff_any(dump=None):
    """
    Sniff any first upcoming packet and return it.

    @type dump: C{str}
    @param dump: path to file where store the result
    """

    return sniff(1, device='any', dump=dump)

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

    packets = []
    for i, pkt in enumerate(f):
        if i == count and count > 0:
            break
        p = decode(pkt[1], f.datalink())
        packets.append(p)
    return packets

def from_file_loop(filename, count=0, filter=None, callback=None,
                                                callback_args=None):
    """
    Load data from pcap file instead of sniffing online.

    Call callback for each or return list of packets.

    @note: sniffed packets in callback function is not decoded.
    To get decoded packets use umit.umpa.protocols._decoder.decode() function
    or other sniff's functions (without a loop feature).

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

    if callback is None:
        raise UMPASniffingException("no callback function is passed.")

    if callback_args is None:
        callback_args = []

    if os.path.isfile(filename):
        f = lpcap.open_pcap(filename)
    else:
        raise UMPASniffingException("can't open file: %s" % filename)

    if filter:
        f.setfilter(filter)

    for i, p in enumerate(f):
        if i == count and count > 0:
            break
        ts, pkt = p
        decoded_pkt = decode(pkt, f.datalink())
        callback(ts, decoded_pkt, *callback_args)

def to_file(fname, count, filter=None, device=None, timeout=0, snaplen=1024,
                                                                promisc=True):
    """
    Sniff packets and store them into a file.

    @type fname: C{str}
    @param fname: path to a file

    @type count: C{int}
    @param count: number of sniffing packets

    @type filter: C{str}
    @param filter: BPF filter

    @type device: C{str}
    @param device: interface for sniffing

    @type timeout: C{int}
    @param timeout: timeout for sniffing

    @type snaplen: C{int}
    @param snaplen: maximum number of bytes to capture of each packet
                    (default: I{1024})

    @type promisc: C{bool}
    @param promisc: promiscous mode sniffing
    """
    sniff(count, filter, device, timeout, snaplen, promisc, fname)
