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

import umpa.protocols._consts as const

from umpa.protocols import *
from umpa.protocols._layer4 import *
from umpa.utils import net
from umpa.utils import bits

class HPort(EnumField):
    bits = 16
    auto = False
    enumerable = {
        "ECHO" : const.PORT_UDP_ECHO
        "DISCARD" : const.PORT_UDP_DISCARD
        "DAYTIME" : const.PORT_UDP_DAYTIME
        "MSP" : const.PORT_UDP_MSP
        "CHARGEN" : const.PORT_UDP_CHARGEN
        "FSP" : const.PORT_UDP_FSP
        "SSH" : const.PORT_UDP_SSH
        "TIME" : const.PORT_UDP_TIME
        "RLP" : const.PORT_UDP_RLP
        "TACACS" : const.PORT_UDP_TACACS
        "CK" : const.PORT_UDP_CK
        "DOMAIN" : const.PORT_UDP_DOMAIN
        "DS" : const.PORT_UDP_DS
        "BOOTPS" : const.PORT_UDP_BOOTPS
        "BOOTPC" : const.PORT_UDP_BOOTPC
        "TFTP" : const.PORT_UDP_TFTP
        "GOPHER" : const.PORT_UDP_GOPHER
        "WWW" : const.PORT_UDP_WWW
        "KERBEROS" : const.PORT_UDP_KERBEROS
        "NEMA" : const.PORT_UDP_NEMA
        "NS" : const.PORT_UDP_NS
        "RTELNET" : const.PORT_UDP_RTELNET
        "POP2" : const.PORT_UDP_POP2
        "POP3" : const.PORT_UDP_POP3
        "SUNRPC" : const.PORT_UDP_SUNRPC
        "NTP" : const.PORT_UDP_NTP
        "PWDGEN" : const.PORT_UDP_PWDGEN
        "SRV" : const.PORT_UDP_SRV
        "NS" : const.PORT_UDP_NS
        "DGM" : const.PORT_UDP_DGM
        "SSN" : const.PORT_UDP_SSN
        "IMAP2" : const.PORT_UDP_IMAP2
        "SNMP" : const.PORT_UDP_SNMP
        "TRAP" : const.PORT_UDP_TRAP
        "MAN" : const.PORT_UDP_MAN
        "AGENT" : const.PORT_UDP_AGENT
        "MAILQ" : const.PORT_UDP_MAILQ
        "XDMCP" : const.PORT_UDP_XDMCP
        "NEXTSTEP" : const.PORT_UDP_NEXTSTEP
        "BGP" : const.PORT_UDP_BGP
        "PROSPERO" : const.PORT_UDP_PROSPERO
        "IRC" : const.PORT_UDP_IRC
        "SMUX" : const.PORT_UDP_SMUX
        "RTMP" : const.PORT_UDP_RTMP
        "NBP" : const.PORT_UDP_NBP
        "ECHO" : const.PORT_UDP_ECHO
        "ZIS" : const.PORT_UDP_ZIS
        "QMTP" : const.PORT_UDP_QMTP
        "Z3950" : const.PORT_UDP_Z3950
        "IPX" : const.PORT_UDP_IPX
        "IMAP3" : const.PORT_UDP_IMAP3
        "PAWSERV" : const.PORT_UDP_PAWSERV
        "ZSERV" : const.PORT_UDP_ZSERV
        "FATSERV" : const.PORT_UDP_FATSERV
        "RPC2PORTMAP" : const.PORT_UDP_RPC2PORTMAP
        "CODAAUTH2" : const.PORT_UDP_CODAAUTH2
        "CLEARCASE" : const.PORT_UDP_CLEARCASE
        "ULISTSERV" : const.PORT_UDP_ULISTSERV
        "LDAP" : const.PORT_UDP_LDAP
        "IMSP" : const.PORT_UDP_IMSP
        "HTTPS" : const.PORT_UDP_HTTPS
        "SNPP" : const.PORT_UDP_SNPP
        "DS" : const.PORT_UDP_DS
        "KPASSWD" : const.PORT_UDP_KPASSWD
        "SAFT" : const.PORT_UDP_SAFT
        "ISAKMP" : const.PORT_UDP_ISAKMP
        "RTSP" : const.PORT_UDP_RTSP
        "NQS" : const.PORT_UDP_NQS
        "LOCAL" : const.PORT_UDP_LOCAL
        "GUI" : const.PORT_UDP_GUI
        "IND" : const.PORT_UDP_IND
        "IPP" : const.PORT_UDP_IPP
        "BIFF" : const.PORT_UDP_BIFF
        "WHO" : const.PORT_UDP_WHO
        "SYSLOG" : const.PORT_UDP_SYSLOG
        "TALK" : const.PORT_UDP_TALK
        "NTALK" : const.PORT_UDP_NTALK
        "ROUTE" : const.PORT_UDP_ROUTE
        "TIMED" : const.PORT_UDP_TIMED
        "NETWALL" : const.PORT_UDP_NETWALL
        "GDOMAP" : const.PORT_UDP_GDOMAP
        "AFPOVERTCP" : const.PORT_UDP_AFPOVERTCP
        "NNTPS" : const.PORT_UDP_NNTPS
        "SUBMISSION" : const.PORT_UDP_SUBMISSION
        "LDAPS" : const.PORT_UDP_LDAPS
        "TINC" : const.PORT_UDP_TINC
        "SILC" : const.PORT_UDP_SILC
        "WEBSTER" : const.PORT_UDP_WEBSTER
        "RSYNC" : const.PORT_UDP_RSYNC
        "TELNETS" : const.PORT_UDP_TELNETS
        "IMAPS" : const.PORT_UDP_IMAPS
        "IRCS" : const.PORT_UDP_IRCS
        "POP3S" : const.PORT_UDP_POP3S
        "SOCKS" : const.PORT_UDP_SOCKS
        "PROOFD" : const.PORT_UDP_PROOFD
        "ROOTD" : const.PORT_UDP_ROOTD
        "OPENVPN" : const.PORT_UDP_OPENVPN
        "RMIREGISTRY" : const.PORT_UDP_RMIREGISTRY
        "KAZAA" : const.PORT_UDP_KAZAA
        "NESSUS" : const.PORT_UDP_NESSUS
        "LOTUSNOTE" : const.PORT_UDP_LOTUSNOTE
        "S" : const.PORT_UDP_S
        "M" : const.PORT_UDP_M
        "INGRESLOCK" : const.PORT_UDP_INGRESLOCK
        "NP" : const.PORT_UDP_NP
        "DATAMETRICS" : const.PORT_UDP_DATAMETRICS
        "PORT" : const.PORT_UDP_PORT
        "KERMIT" : const.PORT_UDP_KERMIT
        "L2F" : const.PORT_UDP_L2F
        "RADIUS" : const.PORT_UDP_RADIUS
        "ACCT" : const.PORT_UDP_ACCT
        "MSNP" : const.PORT_UDP_MSNP
        "NFS" : const.PORT_UDP_NFS
        "SC104" : const.PORT_UDP_SC104
        "CVSPSERVER" : const.PORT_UDP_CVSPSERVER
        "VENUS" : const.PORT_UDP_VENUS
        "SE" : const.PORT_UDP_SE
        "CODASRV" : const.PORT_UDP_CODASRV
        "SE" : const.PORT_UDP_SE
        "MON" : const.PORT_UDP_MON
        "DICT" : const.PORT_UDP_DICT
        "GPSD" : const.PORT_UDP_GPSD
        "GDS_DB" : const.PORT_UDP_GDS_DB
        "ICPV2" : const.PORT_UDP_ICPV2
        "MYSQL" : const.PORT_UDP_MYSQL
        "NUT" : const.PORT_UDP_NUT
        "DISTCC" : const.PORT_UDP_DISTCC
        "DAAP" : const.PORT_UDP_DAAP
        "SVN" : const.PORT_UDP_SVN
        "SUUCP" : const.PORT_UDP_SUUCP
        "SYSRQD" : const.PORT_UDP_SYSRQD
        "IAX" : const.PORT_UDP_IAX
        "PORT" : const.PORT_UDP_PORT
        "RFE" : const.PORT_UDP_RFE
        "MMCC" : const.PORT_UDP_MMCC
        "SIP" : const.PORT_UDP_SIP
        "TLS" : const.PORT_UDP_TLS
        "AOL" : const.PORT_UDP_AOL
        "CLIENT" : const.PORT_UDP_CLIENT
        "SERVER" : const.PORT_UDP_SERVER
        "CFENGINE" : const.PORT_UDP_CFENGINE
        "MDNS" : const.PORT_UDP_MDNS
        "POSTGRESQL" : const.PORT_UDP_POSTGRESQL
        "GGZ" : const.PORT_UDP_GGZ
        "X11" : const.PORT_UDP_X11
        "1" : const.PORT_UDP_1
        "2" : const.PORT_UDP_2
        "3" : const.PORT_UDP_3
        "4" : const.PORT_UDP_4
        "5" : const.PORT_UDP_5
        "6" : const.PORT_UDP_6
        "7" : const.PORT_UDP_7
        "SVC" : const.PORT_UDP_SVC
        "RTR" : const.PORT_UDP_RTR
        "SGE_QMASTER" : const.PORT_UDP_SGE_QMASTER
        "SGE_EXECD" : const.PORT_UDP_SGE_EXECD
        "FILESERVER" : const.PORT_UDP_FILESERVER
        "CALLBACK" : const.PORT_UDP_CALLBACK
        "PRSERVER" : const.PORT_UDP_PRSERVER
        "VLSERVER" : const.PORT_UDP_VLSERVER
        "KASERVER" : const.PORT_UDP_KASERVER
        "VOLSER" : const.PORT_UDP_VOLSER
        "ERRORS" : const.PORT_UDP_ERRORS
        "BOS" : const.PORT_UDP_BOS
        "UPDATE" : const.PORT_UDP_UPDATE
        "RMTSYS" : const.PORT_UDP_RMTSYS
        "SERVICE" : const.PORT_UDP_SERVICE
        "DIR" : const.PORT_UDP_DIR
        "FD" : const.PORT_UDP_FD
        "SD" : const.PORT_UDP_SD
        "AMANDA" : const.PORT_UDP_AMANDA
        "HKP" : const.PORT_UDP_HKP
        "BPRD" : const.PORT_UDP_BPRD
        "BPDBM" : const.PORT_UDP_BPDBM
        "MSVC" : const.PORT_UDP_MSVC
        "VNETD" : const.PORT_UDP_VNETD
        "BPCD" : const.PORT_UDP_BPCD
        "VOPIED" : const.PORT_UDP_VOPIED
        "WNN6" : const.PORT_UDP_WNN6
        "KERBEROS4" : const.PORT_UDP_KERBEROS4
        "KERBEROS_MASTER" : const.PORT_UDP_KERBEROS_MASTER
        "PASSWD_SERVER" : const.PORT_UDP_PASSWD_SERVER
        "SRV" : const.PORT_UDP_SRV
        "CLT" : const.PORT_UDP_CLT
        "HM" : const.PORT_UDP_HM
        "POPPASSD" : const.PORT_UDP_POPPASSD
        "MOIRA_UREG" : const.PORT_UDP_MOIRA_UREG
        "OMIRR" : const.PORT_UDP_OMIRR
        "CUSTOMS" : const.PORT_UDP_CUSTOMS
        "PREDICT" : const.PORT_UDP_PREDICT
        "NINSTALL" : const.PORT_UDP_NINSTALL
        "AFBACKUP" : const.PORT_UDP_AFBACKUP
        "AFMBACKUP" : const.PORT_UDP_AFMBACKUP
        "NOCLOG" : const.PORT_UDP_NOCLOG
        "HOSTMON" : const.PORT_UDP_HOSTMON
        "RPLAY" : const.PORT_UDP_RPLAY
        "RPTP" : const.PORT_UDP_RPTP
        "OMNIORB" : const.PORT_UDP_OMNIORB
        "MANDELSPAWN" : const.PORT_UDP_MANDELSPAWN
        "KAMANDA" : const.PORT_UDP_KAMANDA
        "SMSQP" : const.PORT_UDP_SMSQP
        "XPILOT" : const.PORT_UDP_XPILOT
        "CMSD" : const.PORT_UDP_CMSD
        "CRSD" : const.PORT_UDP_CRSD
        "GCD" : const.PORT_UDP_GCD
        "ISDNLOG" : const.PORT_UDP_ISDNLOG
        "VBOXD" : const.PORT_UDP_VBOXD
        "ASP" : const.PORT_UDP_ASP
    }

class HLength(SpecialIntField):
    """Length  is the length  in octets  of this user datagram  including  this
    header  and the data.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # returns in byte units
        return 8 + self._tmp_value/8    # minimum is 8

class UDP(Protocol):
    """This is User Datagram Protocol.
    
    This protocol  provides  a procedure  for application  programs  to send
    messages  to other programs  with a minimum  of protocol mechanism.  The
    protocol  is transaction oriented, and delivery and duplicate protection
    are not guaranteed.
    """
    layer = 4
    protocol_id = const.PROTOCOL_UDP

    _ordered_fields = ('source_port', 'destination_port', '_length',
                                                            '_checksum')

    def __init__(self, **kw):
        fields_list = [ HPort("Source Port", 0),
                        HPort("Destination Port", 0),
                        HLength("Length"),
                        Layer4ChecksumField("Checksum"), ]

        # we call super.__init__ after prepared necessary data
        super(UDP, self).__init__(fields_list, **kw)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._get_field('source_port').set_doc("The source port number. \
See RFC 768 for more.")
        self._get_field('destination_port').set_doc("The destination port \
number. See RFC 768 for more.")
        self._get_field('_checksum').set_doc("Checksum of Pseudo Header, UDP \
header and data. See RFC 768 for more.")

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        # Length
        self._get_field('_checksum')._tmp_value = protocol_bits

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        cksum_rev_offset = 0
        # checking if user not defined his own value of checksum
        if bits.get_bits(raw_value, self._get_field('_checksum').bits,
                                    cksum_rev_offset, rev_offset=True) == 0:
            # Payload
            if self.payload:
                cksum = self.payload.__raw_value
            else:
                cksum = 0
            offset = protocol_bits

            # UDP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # create pseudo header object
            pheader = PseudoHeader(self.protocol_id,
                                        self._get_field('_length').fillout())
            # generate raw value of it
            pheader_bits = pheader._get_raw(protocol_container,
                                                        protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_bits << offset

            # finally, calcute and apply checksum
            raw_cksum = net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_rev_offset

        return raw_value, bit

protocols = [ UDP, ]
