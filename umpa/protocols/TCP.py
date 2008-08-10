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
        "TCPMUX" : const.PORT_TCP_TCPMUX
        "ECHO" : const.PORT_TCP_ECHO
        "DISCARD" : const.PORT_TCP_DISCARD
        "SYSTAT" : const.PORT_TCP_SYSTAT
        "DAYTIME" : const.PORT_TCP_DAYTIME
        "NETSTAT" : const.PORT_TCP_NETSTAT
        "QOTD" : const.PORT_TCP_QOTD
        "MSP" : const.PORT_TCP_MSP
        "CHARGEN" : const.PORT_TCP_CHARGEN
        "DATA" : const.PORT_TCP_DATA
        "FTP" : const.PORT_TCP_FTP
        "SSH" : const.PORT_TCP_SSH
        "TELNET" : const.PORT_TCP_TELNET
        "SMTP" : const.PORT_TCP_SMTP
        "TIME" : const.PORT_TCP_TIME
        "NAMESERVER" : const.PORT_TCP_NAMESERVER
        "WHOIS" : const.PORT_TCP_WHOIS
        "TACACS" : const.PORT_TCP_TACACS
        "CK" : const.PORT_TCP_CK
        "DOMAIN" : const.PORT_TCP_DOMAIN
        "MTP" : const.PORT_TCP_MTP
        "DS" : const.PORT_TCP_DS
        "BOOTPS" : const.PORT_TCP_BOOTPS
        "BOOTPC" : const.PORT_TCP_BOOTPC
        "GOPHER" : const.PORT_TCP_GOPHER
        "RJE" : const.PORT_TCP_RJE
        "FINGER" : const.PORT_TCP_FINGER
        "WWW" : const.PORT_TCP_WWW
        "LINK" : const.PORT_TCP_LINK
        "KERBEROS" : const.PORT_TCP_KERBEROS
        "SUPDUP" : const.PORT_TCP_SUPDUP
        "HOSTNAMES" : const.PORT_TCP_HOSTNAMES
        "TSAP" : const.PORT_TCP_TSAP
        "NEMA" : const.PORT_TCP_NEMA
        "NS" : const.PORT_TCP_NS
        "RTELNET" : const.PORT_TCP_RTELNET
        "POP2" : const.PORT_TCP_POP2
        "POP3" : const.PORT_TCP_POP3
        "SUNRPC" : const.PORT_TCP_SUNRPC
        "AUTH" : const.PORT_TCP_AUTH
        "SFTP" : const.PORT_TCP_SFTP
        "PATH" : const.PORT_TCP_PATH
        "NNTP" : const.PORT_TCP_NNTP
        "NTP" : const.PORT_TCP_NTP
        "PWDGEN" : const.PORT_TCP_PWDGEN
        "SRV" : const.PORT_TCP_SRV
        "NS" : const.PORT_TCP_NS
        "DGM" : const.PORT_TCP_DGM
        "SSN" : const.PORT_TCP_SSN
        "IMAP2" : const.PORT_TCP_IMAP2
        "SNMP" : const.PORT_TCP_SNMP
        "TRAP" : const.PORT_TCP_TRAP
        "MAN" : const.PORT_TCP_MAN
        "AGENT" : const.PORT_TCP_AGENT
        "MAILQ" : const.PORT_TCP_MAILQ
        "XDMCP" : const.PORT_TCP_XDMCP
        "NEXTSTEP" : const.PORT_TCP_NEXTSTEP
        "BGP" : const.PORT_TCP_BGP
        "PROSPERO" : const.PORT_TCP_PROSPERO
        "IRC" : const.PORT_TCP_IRC
        "SMUX" : const.PORT_TCP_SMUX
        "RTMP" : const.PORT_TCP_RTMP
        "NBP" : const.PORT_TCP_NBP
        "ECHO" : const.PORT_TCP_ECHO
        "ZIS" : const.PORT_TCP_ZIS
        "QMTP" : const.PORT_TCP_QMTP
        "Z3950" : const.PORT_TCP_Z3950
        "IPX" : const.PORT_TCP_IPX
        "IMAP3" : const.PORT_TCP_IMAP3
        "PAWSERV" : const.PORT_TCP_PAWSERV
        "ZSERV" : const.PORT_TCP_ZSERV
        "FATSERV" : const.PORT_TCP_FATSERV
        "RPC2PORTMAP" : const.PORT_TCP_RPC2PORTMAP
        "CODAAUTH2" : const.PORT_TCP_CODAAUTH2
        "CLEARCASE" : const.PORT_TCP_CLEARCASE
        "ULISTSERV" : const.PORT_TCP_ULISTSERV
        "LDAP" : const.PORT_TCP_LDAP
        "IMSP" : const.PORT_TCP_IMSP
        "HTTPS" : const.PORT_TCP_HTTPS
        "SNPP" : const.PORT_TCP_SNPP
        "DS" : const.PORT_TCP_DS
        "KPASSWD" : const.PORT_TCP_KPASSWD
        "SAFT" : const.PORT_TCP_SAFT
        "ISAKMP" : const.PORT_TCP_ISAKMP
        "RTSP" : const.PORT_TCP_RTSP
        "NQS" : const.PORT_TCP_NQS
        "LOCAL" : const.PORT_TCP_LOCAL
        "GUI" : const.PORT_TCP_GUI
        "IND" : const.PORT_TCP_IND
        "IPP" : const.PORT_TCP_IPP
        "EXEC" : const.PORT_TCP_EXEC
        "LOGIN" : const.PORT_TCP_LOGIN
        "SHELL" : const.PORT_TCP_SHELL
        "PRINTER" : const.PORT_TCP_PRINTER
        "TEMPO" : const.PORT_TCP_TEMPO
        "COURIER" : const.PORT_TCP_COURIER
        "CONFERENCE" : const.PORT_TCP_CONFERENCE
        "NETNEWS" : const.PORT_TCP_NETNEWS
        "GDOMAP" : const.PORT_TCP_GDOMAP
        "UUCP" : const.PORT_TCP_UUCP
        "KLOGIN" : const.PORT_TCP_KLOGIN
        "KSHELL" : const.PORT_TCP_KSHELL
        "AFPOVERTCP" : const.PORT_TCP_AFPOVERTCP
        "REMOTEFS" : const.PORT_TCP_REMOTEFS
        "NNTPS" : const.PORT_TCP_NNTPS
        "SUBMISSION" : const.PORT_TCP_SUBMISSION
        "LDAPS" : const.PORT_TCP_LDAPS
        "TINC" : const.PORT_TCP_TINC
        "SILC" : const.PORT_TCP_SILC
        "ADM" : const.PORT_TCP_ADM
        "WEBSTER" : const.PORT_TCP_WEBSTER
        "RSYNC" : const.PORT_TCP_RSYNC
        "DATA" : const.PORT_TCP_DATA
        "FTPS" : const.PORT_TCP_FTPS
        "TELNETS" : const.PORT_TCP_TELNETS
        "IMAPS" : const.PORT_TCP_IMAPS
        "IRCS" : const.PORT_TCP_IRCS
        "POP3S" : const.PORT_TCP_POP3S
        "SOCKS" : const.PORT_TCP_SOCKS
        "PROOFD" : const.PORT_TCP_PROOFD
        "ROOTD" : const.PORT_TCP_ROOTD
        "OPENVPN" : const.PORT_TCP_OPENVPN
        "RMIREGISTRY" : const.PORT_TCP_RMIREGISTRY
        "KAZAA" : const.PORT_TCP_KAZAA
        "NESSUS" : const.PORT_TCP_NESSUS
        "LOTUSNOTE" : const.PORT_TCP_LOTUSNOTE
        "S" : const.PORT_TCP_S
        "M" : const.PORT_TCP_M
        "INGRESLOCK" : const.PORT_TCP_INGRESLOCK
        "NP" : const.PORT_TCP_NP
        "DATAMETRICS" : const.PORT_TCP_DATAMETRICS
        "PORT" : const.PORT_TCP_PORT
        "KERMIT" : const.PORT_TCP_KERMIT
        "L2F" : const.PORT_TCP_L2F
        "RADIUS" : const.PORT_TCP_RADIUS
        "ACCT" : const.PORT_TCP_ACCT
        "MSNP" : const.PORT_TCP_MSNP
        "STATUS" : const.PORT_TCP_STATUS
        "SERVER" : const.PORT_TCP_SERVER
        "REMOTEPING" : const.PORT_TCP_REMOTEPING
        "NFS" : const.PORT_TCP_NFS
        "SC104" : const.PORT_TCP_SC104
        "CVSPSERVER" : const.PORT_TCP_CVSPSERVER
        "VENUS" : const.PORT_TCP_VENUS
        "SE" : const.PORT_TCP_SE
        "CODASRV" : const.PORT_TCP_CODASRV
        "SE" : const.PORT_TCP_SE
        "MON" : const.PORT_TCP_MON
        "DICT" : const.PORT_TCP_DICT
        "GPSD" : const.PORT_TCP_GPSD
        "GDS_DB" : const.PORT_TCP_GDS_DB
        "ICPV2" : const.PORT_TCP_ICPV2
        "MYSQL" : const.PORT_TCP_MYSQL
        "NUT" : const.PORT_TCP_NUT
        "DISTCC" : const.PORT_TCP_DISTCC
        "DAAP" : const.PORT_TCP_DAAP
        "SVN" : const.PORT_TCP_SVN
        "SUUCP" : const.PORT_TCP_SUUCP
        "SYSRQD" : const.PORT_TCP_SYSRQD
        "IAX" : const.PORT_TCP_IAX
        "PORT" : const.PORT_TCP_PORT
        "RFE" : const.PORT_TCP_RFE
        "MMCC" : const.PORT_TCP_MMCC
        "SIP" : const.PORT_TCP_SIP
        "TLS" : const.PORT_TCP_TLS
        "AOL" : const.PORT_TCP_AOL
        "CLIENT" : const.PORT_TCP_CLIENT
        "SERVER" : const.PORT_TCP_SERVER
        "CFENGINE" : const.PORT_TCP_CFENGINE
        "MDNS" : const.PORT_TCP_MDNS
        "POSTGRESQL" : const.PORT_TCP_POSTGRESQL
        "GGZ" : const.PORT_TCP_GGZ
        "X11" : const.PORT_TCP_X11
        "1" : const.PORT_TCP_1
        "2" : const.PORT_TCP_2
        "3" : const.PORT_TCP_3
        "4" : const.PORT_TCP_4
        "5" : const.PORT_TCP_5
        "6" : const.PORT_TCP_6
        "7" : const.PORT_TCP_7
        "SVC" : const.PORT_TCP_SVC
        "RTR" : const.PORT_TCP_RTR
        "SGE_QMASTER" : const.PORT_TCP_SGE_QMASTER
        "SGE_EXECD" : const.PORT_TCP_SGE_EXECD
        "FILESERVER" : const.PORT_TCP_FILESERVER
        "CALLBACK" : const.PORT_TCP_CALLBACK
        "PRSERVER" : const.PORT_TCP_PRSERVER
        "VLSERVER" : const.PORT_TCP_VLSERVER
        "KASERVER" : const.PORT_TCP_KASERVER
        "VOLSER" : const.PORT_TCP_VOLSER
        "ERRORS" : const.PORT_TCP_ERRORS
        "BOS" : const.PORT_TCP_BOS
        "UPDATE" : const.PORT_TCP_UPDATE
        "RMTSYS" : const.PORT_TCP_RMTSYS
        "SERVICE" : const.PORT_TCP_SERVICE
        "DIR" : const.PORT_TCP_DIR
        "FD" : const.PORT_TCP_FD
        "SD" : const.PORT_TCP_SD
        "AMANDA" : const.PORT_TCP_AMANDA
        "HKP" : const.PORT_TCP_HKP
        "BPRD" : const.PORT_TCP_BPRD
        "BPDBM" : const.PORT_TCP_BPDBM
        "MSVC" : const.PORT_TCP_MSVC
        "VNETD" : const.PORT_TCP_VNETD
        "BPCD" : const.PORT_TCP_BPCD
        "VOPIED" : const.PORT_TCP_VOPIED
        "WNN6" : const.PORT_TCP_WNN6
        "KERBEROS4" : const.PORT_TCP_KERBEROS4
        "KERBEROS_MASTER" : const.PORT_TCP_KERBEROS_MASTER
        "KRB_PROP" : const.PORT_TCP_KRB_PROP
        "KRBUPDATE" : const.PORT_TCP_KRBUPDATE
        "SWAT" : const.PORT_TCP_SWAT
        "KPOP" : const.PORT_TCP_KPOP
        "KNETD" : const.PORT_TCP_KNETD
        "EKLOGIN" : const.PORT_TCP_EKLOGIN
        "KX" : const.PORT_TCP_KX
        "IPROP" : const.PORT_TCP_IPROP
        "SUPFILESRV" : const.PORT_TCP_SUPFILESRV
        "SUPFILEDBG" : const.PORT_TCP_SUPFILEDBG
        "LINUXCONF" : const.PORT_TCP_LINUXCONF
        "POPPASSD" : const.PORT_TCP_POPPASSD
        "SSMTP" : const.PORT_TCP_SSMTP
        "MOIRA_DB" : const.PORT_TCP_MOIRA_DB
        "MOIRA_UPDATE" : const.PORT_TCP_MOIRA_UPDATE
        "SPAMD" : const.PORT_TCP_SPAMD
        "OMIRR" : const.PORT_TCP_OMIRR
        "CUSTOMS" : const.PORT_TCP_CUSTOMS
        "SKKSERV" : const.PORT_TCP_SKKSERV
        "RMTCFG" : const.PORT_TCP_RMTCFG
        "WIPLD" : const.PORT_TCP_WIPLD
        "XTEL" : const.PORT_TCP_XTEL
        "XTELW" : const.PORT_TCP_XTELW
        "SUPPORT" : const.PORT_TCP_SUPPORT
        "SIEVE" : const.PORT_TCP_SIEVE
        "CFINGER" : const.PORT_TCP_CFINGER
        "NDTP" : const.PORT_TCP_NDTP
        "FROX" : const.PORT_TCP_FROX
        "NINSTALL" : const.PORT_TCP_NINSTALL
        "ZEBRASRV" : const.PORT_TCP_ZEBRASRV
        "ZEBRA" : const.PORT_TCP_ZEBRA
        "RIPD" : const.PORT_TCP_RIPD
        "RIPNGD" : const.PORT_TCP_RIPNGD
        "OSPFD" : const.PORT_TCP_OSPFD
        "BGPD" : const.PORT_TCP_BGPD
        "OSPF6D" : const.PORT_TCP_OSPF6D
        "OSPFAPI" : const.PORT_TCP_OSPFAPI
        "ISISD" : const.PORT_TCP_ISISD
        "AFBACKUP" : const.PORT_TCP_AFBACKUP
        "AFMBACKUP" : const.PORT_TCP_AFMBACKUP
        "XTELL" : const.PORT_TCP_XTELL
        "FAX" : const.PORT_TCP_FAX
        "HYLAFAX" : const.PORT_TCP_HYLAFAX
        "DISTMP3" : const.PORT_TCP_DISTMP3
        "MUNIN" : const.PORT_TCP_MUNIN
        "CSTATD" : const.PORT_TCP_CSTATD
        "SSTATD" : const.PORT_TCP_SSTATD
        "PCRD" : const.PORT_TCP_PCRD
        "NOCLOG" : const.PORT_TCP_NOCLOG
        "HOSTMON" : const.PORT_TCP_HOSTMON
        "RPLAY" : const.PORT_TCP_RPLAY
        "RPTP" : const.PORT_TCP_RPTP
        "NSCA" : const.PORT_TCP_NSCA
        "MRTD" : const.PORT_TCP_MRTD
        "BGPSIM" : const.PORT_TCP_BGPSIM
        "CANNA" : const.PORT_TCP_CANNA
        "PORT" : const.PORT_TCP_PORT
        "IRCD" : const.PORT_TCP_IRCD
        "FTP" : const.PORT_TCP_FTP
        "WEBCACHE" : const.PORT_TCP_WEBCACHE
        "TPROXY" : const.PORT_TCP_TPROXY
        "OMNIORB" : const.PORT_TCP_OMNIORB
        "DAEMON" : const.PORT_TCP_DAEMON
        "XINETD" : const.PORT_TCP_XINETD
        "GIT" : const.PORT_TCP_GIT
        "ZOPE" : const.PORT_TCP_ZOPE
        "WEBMIN" : const.PORT_TCP_WEBMIN
        "KAMANDA" : const.PORT_TCP_KAMANDA
        "AMANDAIDX" : const.PORT_TCP_AMANDAIDX
        "AMIDXTAPE" : const.PORT_TCP_AMIDXTAPE
        "SMSQP" : const.PORT_TCP_SMSQP
        "XPILOT" : const.PORT_TCP_XPILOT
        "CAD" : const.PORT_TCP_CAD
        "ISDNLOG" : const.PORT_TCP_ISDNLOG
        "VBOXD" : const.PORT_TCP_VBOXD
        "BINKP" : const.PORT_TCP_BINKP
        "ASP" : const.PORT_TCP_ASP
        "CSYNC2" : const.PORT_TCP_CSYNC2
        "DIRCPROXY" : const.PORT_TCP_DIRCPROXY
        "TFIDO" : const.PORT_TCP_TFIDO
        "FIDO" : const.PORT_TCP_FIDO
    }

class HSequenceNumber(IntField):
    """The sequence number of the first data octet in this segment (except
    when SYN is present).

    See RFC 793 for more.
    """
    bits = 32
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class HAcknowledgmentNumber(IntField):
    """If the ACK control bit is set this field contains the value of the
    next sequence number the sender of the segment is expecting to receive.

    See RFC 793 for more.
    """
    bits = 32
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 1

class HDataOffset(SpecialIntField):
    """The number of 32 bit words in the TCP Header. This indicates where
    the data begins.

    See RFC 793 for more.
    """
    bits = 4
    auto = True
    def _generate_value(self):
        # returns in 32-bits units
        return 5 + self._tmp_value / 32 # 5 is a minimum value

class HReserved(IntField):
    """Reserved for future use.

    See RFC 793 for more.
    """
    bits = 6
    auto = True
    def _generate_value(self):
        return 0

class HWindow(IntField):
    """The number of data octets beginning with the one indicated in the
    acknowledgment field which the sender of this segment is willing to accept.

    See RFC 793 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 512

class HUrgentPointer(IntField):
    """This field communicates the current value of the urgent pointer as a
    positive offset from the sequence number in this segment.

    See RFC 793 for more.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class TCP(Protocol):
    """This is Transmission Control Protocol.
    It the most common protocol in the Internet on fourth layer
    of the OSI model.
    """
    layer = 4       # layer of the OSI
    protocol_id = const.PROTOCOL_TCP
    name = "TCP"

    _ordered_fields = ('source_port', 'destination_port', '_sequence_number',
                    '_acknowledgment_number', '_data_offset', '_reserved',
                    'control_bits', '_window', '_checksum', '_urgent_pointer',
                    'options', '_padding',)

    def __init__(self, **kw):
        control_bits = ('urg', 'ack', 'psh', 'rst', 'syn', 'fin')
        control_bits_predefined = dict.fromkeys(control_bits, 0)

        fields_list = [ HPort("Source Port", 0),
                        HPort("Destination Port", 0),
                        HSequenceNumber("Sequence Number"),
                        HAcknowledgmentNumber("Acknowledgment Number"),
                        HDataOffset("DataOffset"), HReserved("Reserved", 0),
                        Flags("Control Bits", control_bits,
                        **control_bits_predefined),
                        HWindow("Window"), Layer4ChecksumField("Checksum"),
                        HUrgentPointer("Urgent Pointer"), Flags("Options", ()),
                        PaddingField("Padding") ]

        # we call super.__init__ after prepared necessary data
        super(TCP, self).__init__(fields_list, **kw)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self._get_field('source_port').set_doc("The source port number. \
See RFC 793 for more.")
        self._get_field('destination_port').set_doc("The destination port \
number. See RFC 793 for more.")
        self._get_field('control_bits').set_doc("URG, ACK, PSH, RST, SYN, FIN \
flags. See RFC 793 for more.")
        self._get_field('_checksum').set_doc("Checksum of Pseudo Header, TCP \
header and data. See RFC 793 for more.")
        self._get_field('options').set_doc("Options may occupy space at the \
end of the TCP header and are a multiple of 8 bits in length. See RFC 793 \
for more.")
        self._get_field('_padding').set_doc("The TCP header padding is used \
to ensure that the TCP header ends and data begins on a 32 bit boundary. \
See RFC 793 for more.")

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        # Padding
        self._get_field('_padding')._tmp_value = \
                                                self._get_field('options').bits

        # Data Offset
        self._get_field('_data_offset')._tmp_value = \
            self._get_field('options').bits + self._get_field('_padding').bits

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        # rev_offset it the offset from the right side
        cksum_rev_offset = bit - self.get_offset('_checksum') - \
                                            self._get_field('_checksum').bits
        # checking if user not defined his own value of checksum
        if bits.get_bits(raw_value, self._get_field('_checksum').bits,
                                    cksum_rev_offset, rev_offset=True) == 0:
            # Payload
            if self.payload:
                cksum = self.payload.__raw_value
            else:
                cksum = 0
            offset = protocol_bits

            # TCP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # TCP header length...converted to bits unit
            total_length = self._get_field('_data_offset').fillout()*32
            # add payload
            total_length += protocol_bits
            # conversion to bytes unit
            total_length /= 8

            # create pseudo header object
            pheader = PseudoHeader(self.protocol_id, total_length)
            # generate raw value of it
            pheader_bits = pheader._get_raw(protocol_container,
                                                        protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_bits << offset

            # finally, calcute and apply checksum
            raw_cksum = net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_rev_offset

        return raw_value, bit

protocols = [ TCP, ]
