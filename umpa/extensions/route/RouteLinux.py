#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: Luís A. Bastião Silva <luis.kop@gmail.com>
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

import struct, socket, string
from fcntl import ioctl
import re

from umpa.utils.net import parse_ipv4
from umpa.extensions.route.RouteAbstract import RouteAbstract
"""
The goal of this extension is support an abstraction to 
Routing Tables of kernel. 
"""

# From linux/sockios.h
SIOCGIFADDR = 0x8915  # get PA address
SIOCADDRT = 0x890B    # add routing table entry
SIOCDELRT = 0x890C    #delete routing table entry

# From linux/route.h
RTF_UP = 0x0001       # route usable
RTF_GATEWAY = 0x0002  # destination is a gateway
RTF_HOST = 0x0004     # host entry (net otherwise)



PROC_ROUTE="/proc/net/route"
PROC_ROUTE6="/proc/net/route6"


class RouteEntry:
    """
    Routing Entry implementation 
    
    rtentry - structure of an entry in the kernel routing table 
    This implementation simulate the rtentry in Linux Kernel
    
    
    struct rtentry 
    {
	unsigned long	rt_pad1;
	struct sockaddr	rt_dst;		/* target address		*/
	struct sockaddr	rt_gateway;	/* gateway addr (RTF_GATEWAY)	*/
	struct sockaddr	rt_genmask;	/* target network mask (IP)	*/
	unsigned short	rt_flags;
	short		rt_pad2;
	unsigned long	rt_pad3;
	void		*rt_pad4;
	short		rt_metric;	/* +1 for binary compatibility!	*/
	char *rt_dev;	/* forcing the device at add	*/
	unsigned long	rt_mtu;		/* per route MTU/Window 	*/
	unsigned long	rt_window;	/* Window clamping 		*/
	unsigned short	rt_irtt;	/* Initial RTT			*/
    };
    struct sockaddr {
	sa_family_t	sa_family;	/* address family, AF_xxx	*/
	char		sa_data[14];	/* 14 bytes of protocol address	*/
    };

    """
    def __init__(self,dst,mask,gw,flags, dev="" ):
	"""
	Create a new Route Entry
	"""
	self._rt_flags = flags
	self._rt_dst = dst 
	self._rt_gateway = gw 
	self._rt_genmask = mask
	self._rt_dev = dev
    def encode(self):
	pad1 = [0]
	padding = [ 0,0,0,0,0,0,0,0]
	socket_family = [socket.AF_INET]
	dst =  socket_family + parse_ipv4(self._rt_dst) + padding
	gw =  socket_family + parse_ipv4(self._rt_gateway) + padding
	mask = socket_family + parse_ipv4(self._rt_genmask) + padding	
	pad2 = [0]
	pad3 = [0]
	pad4 = [0]
	metric = [0]
	dev = [self._rt_dev]
	mtu = [0]
	window = [0]
	irtt = [0]
	
	fields = pad1 + dst + gw + mask + [self._rt_flags] 
	fields += pad2 +  pad3 + pad4 +  metric + dev + mtu + window + irtt 
	s = struct.pack('LL12BL12BL12BHhLPhsLLL', 
			*fields)
	return s 
    
    
    
class Route(RouteAbstract):
    def __init__(self):
        RouteAbstract.__init__(self)

    def add(self, dst, mask, gw, dev=''):
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	    rt = RouteEntry(dst, mask, gw , RTF_GATEWAY | RTF_UP , dev)
	    enc = rt.encode()
	    r = ioctl(s, SIOCADDRT,enc) 

	except IOError:
                pass
    def delete(self, dst):
	try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    rt = RouteEntry(dst, "255.255.255.255", "0.0.0.0" ,
			    RTF_UP | RTF_HOST)
	    
	    enc = rt.encode()
	    r = ioctl(s, SIOCDELRT,enc) 

	except IOError:
                pass
    def _get_ip(self, ip):
	stack = []
	i = 0
	last_char = ''
	for c in str(ip):
	    if i%2 == 0:
		last_char = c
	    else:
		stack.append(int(last_char+c, 16))
	    i+=1
	ip_addr=str(stack.pop())
	while len(stack) > 0:
	    ip_addr+="."+str(stack.pop())
	return ip_addr

    def get_routes(self):
        
        # Format
        # dic: {dst, gw, mask, dev, out}
        routes = []
        
        # Try use SIOCRTMSG is waste time (does not work for propose)	
        f = file(PROC_ROUTE)
	
        
        f.readline() # Pass header line
        for line in f.readlines():
            dev,dst,gw,flags,refct,use,metric,mask,mss,win,irtt = line.split()
	    
            # Get output
            # Based on "Unix Network Programming" 
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # It is similar in C:
            #  ioctl_result=ioctl(_socket,
            #         SIOCGIFADDR,
            #         (char *)&data
            #   );
            try:
                ifreq = ioctl(s, SIOCGIFADDR,struct.pack("16s16x",dev))
            except IOError:
		continue
	    out = string.join(map(str,map(ord,ifreq[20:24])),'.')
	    dst = self._get_ip(dst)
	    gw = self._get_ip(gw)
	    mask = self._get_ip(mask)
	    routes.append({'dst':dst, 'gw':gw,
                           'mask': mask,
                           'dev':dev, 'out':out})
        return routes
            

    