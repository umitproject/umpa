#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008-2009 Adriano Monteiro Marques.
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

"""
TCP (Transmission Control Protocol) protocol implementation.
"""

from umpa.protocols import _consts
from umpa.protocols import _fields
from umpa.protocols import _protocols
from umpa.protocols import _layer4
import umpa.utils.net as _net
import umpa.utils.bits as _bits

__all__ = [ "TCP", ]

class _HPort(_fields.EnumField):
    """
    TCP uses the notion of port numbers to identify sending and receiving
    application end-points on a host, or Internet sockets.
    """

    bits = 16
    auto = False
    enumerable = {
        "TCPMUX" : _consts.PORT_TCP_TCPMUX,
        "ECHO" : _consts.PORT_TCP_ECHO,
        "DISCARD" : _consts.PORT_TCP_DISCARD,
        "SYSTAT" : _consts.PORT_TCP_SYSTAT,
        "DAYTIME" : _consts.PORT_TCP_DAYTIME,
        "NETSTAT" : _consts.PORT_TCP_NETSTAT,
        "QOTD" : _consts.PORT_TCP_QOTD,
        "MSP" : _consts.PORT_TCP_MSP,
        "CHARGEN" : _consts.PORT_TCP_CHARGEN,
        "DATA" : _consts.PORT_TCP_DATA,
        "FTP" : _consts.PORT_TCP_FTP,
        "SSH" : _consts.PORT_TCP_SSH,
        "TELNET" : _consts.PORT_TCP_TELNET,
        "SMTP" : _consts.PORT_TCP_SMTP,
        "TIME" : _consts.PORT_TCP_TIME,
        "NAMESERVER" : _consts.PORT_TCP_NAMESERVER,
        "WHOIS" : _consts.PORT_TCP_WHOIS,
        "TACACS" : _consts.PORT_TCP_TACACS,
        "CK" : _consts.PORT_TCP_CK,
        "DOMAIN" : _consts.PORT_TCP_DOMAIN,
        "MTP" : _consts.PORT_TCP_MTP,
        "DS" : _consts.PORT_TCP_DS,
        "BOOTPS" : _consts.PORT_TCP_BOOTPS,
        "BOOTPC" : _consts.PORT_TCP_BOOTPC,
        "GOPHER" : _consts.PORT_TCP_GOPHER,
        "RJE" : _consts.PORT_TCP_RJE,
        "FINGER" : _consts.PORT_TCP_FINGER,
        "WWW" : _consts.PORT_TCP_WWW,
        "LINK" : _consts.PORT_TCP_LINK,
        "KERBEROS" : _consts.PORT_TCP_KERBEROS,
        "SUPDUP" : _consts.PORT_TCP_SUPDUP,
        "HOSTNAMES" : _consts.PORT_TCP_HOSTNAMES,
        "TSAP" : _consts.PORT_TCP_TSAP,
        "NEMA" : _consts.PORT_TCP_NEMA,
        "NS" : _consts.PORT_TCP_NS,
        "RTELNET" : _consts.PORT_TCP_RTELNET,
        "POP2" : _consts.PORT_TCP_POP2,
        "POP3" : _consts.PORT_TCP_POP3,
        "SUNRPC" : _consts.PORT_TCP_SUNRPC,
        "AUTH" : _consts.PORT_TCP_AUTH,
        "SFTP" : _consts.PORT_TCP_SFTP,
        "PATH" : _consts.PORT_TCP_PATH,
        "NNTP" : _consts.PORT_TCP_NNTP,
        "NTP" : _consts.PORT_TCP_NTP,
        "PWDGEN" : _consts.PORT_TCP_PWDGEN,
        "SRV" : _consts.PORT_TCP_SRV,
        "NS" : _consts.PORT_TCP_NS,
        "DGM" : _consts.PORT_TCP_DGM,
        "SSN" : _consts.PORT_TCP_SSN,
        "IMAP2" : _consts.PORT_TCP_IMAP2,
        "SNMP" : _consts.PORT_TCP_SNMP,
        "TRAP" : _consts.PORT_TCP_TRAP,
        "MAN" : _consts.PORT_TCP_MAN,
        "AGENT" : _consts.PORT_TCP_AGENT,
        "MAILQ" : _consts.PORT_TCP_MAILQ,
        "XDMCP" : _consts.PORT_TCP_XDMCP,
        "NEXTSTEP" : _consts.PORT_TCP_NEXTSTEP,
        "BGP" : _consts.PORT_TCP_BGP,
        "PROSPERO" : _consts.PORT_TCP_PROSPERO,
        "IRC" : _consts.PORT_TCP_IRC,
        "SMUX" : _consts.PORT_TCP_SMUX,
        "RTMP" : _consts.PORT_TCP_RTMP,
        "NBP" : _consts.PORT_TCP_NBP,
        "ECHO" : _consts.PORT_TCP_ECHO,
        "ZIS" : _consts.PORT_TCP_ZIS,
        "QMTP" : _consts.PORT_TCP_QMTP,
        "Z3950" : _consts.PORT_TCP_Z3950,
        "IPX" : _consts.PORT_TCP_IPX,
        "IMAP3" : _consts.PORT_TCP_IMAP3,
        "PAWSERV" : _consts.PORT_TCP_PAWSERV,
        "ZSERV" : _consts.PORT_TCP_ZSERV,
        "FATSERV" : _consts.PORT_TCP_FATSERV,
        "RPC2PORTMAP" : _consts.PORT_TCP_RPC2PORTMAP,
        "CODAAUTH2" : _consts.PORT_TCP_CODAAUTH2,
        "CLEARCASE" : _consts.PORT_TCP_CLEARCASE,
        "ULISTSERV" : _consts.PORT_TCP_ULISTSERV,
        "LDAP" : _consts.PORT_TCP_LDAP,
        "IMSP" : _consts.PORT_TCP_IMSP,
        "HTTPS" : _consts.PORT_TCP_HTTPS,
        "SNPP" : _consts.PORT_TCP_SNPP,
        "DS" : _consts.PORT_TCP_DS,
        "KPASSWD" : _consts.PORT_TCP_KPASSWD,
        "SAFT" : _consts.PORT_TCP_SAFT,
        "ISAKMP" : _consts.PORT_TCP_ISAKMP,
        "RTSP" : _consts.PORT_TCP_RTSP,
        "NQS" : _consts.PORT_TCP_NQS,
        "LOCAL" : _consts.PORT_TCP_LOCAL,
        "GUI" : _consts.PORT_TCP_GUI,
        "IND" : _consts.PORT_TCP_IND,
        "IPP" : _consts.PORT_TCP_IPP,
        "EXEC" : _consts.PORT_TCP_EXEC,
        "LOGIN" : _consts.PORT_TCP_LOGIN,
        "SHELL" : _consts.PORT_TCP_SHELL,
        "PRINTER" : _consts.PORT_TCP_PRINTER,
        "TEMPO" : _consts.PORT_TCP_TEMPO,
        "COURIER" : _consts.PORT_TCP_COURIER,
        "CONFERENCE" : _consts.PORT_TCP_CONFERENCE,
        "NETNEWS" : _consts.PORT_TCP_NETNEWS,
        "GDOMAP" : _consts.PORT_TCP_GDOMAP,
        "UUCP" : _consts.PORT_TCP_UUCP,
        "KLOGIN" : _consts.PORT_TCP_KLOGIN,
        "KSHELL" : _consts.PORT_TCP_KSHELL,
        "AFPOVERTCP" : _consts.PORT_TCP_AFPOVERTCP,
        "REMOTEFS" : _consts.PORT_TCP_REMOTEFS,
        "NNTPS" : _consts.PORT_TCP_NNTPS,
        "SUBMISSION" : _consts.PORT_TCP_SUBMISSION,
        "LDAPS" : _consts.PORT_TCP_LDAPS,
        "TINC" : _consts.PORT_TCP_TINC,
        "SILC" : _consts.PORT_TCP_SILC,
        "ADM" : _consts.PORT_TCP_ADM,
        "WEBSTER" : _consts.PORT_TCP_WEBSTER,
        "RSYNC" : _consts.PORT_TCP_RSYNC,
        "DATA" : _consts.PORT_TCP_DATA,
        "FTPS" : _consts.PORT_TCP_FTPS,
        "TELNETS" : _consts.PORT_TCP_TELNETS,
        "IMAPS" : _consts.PORT_TCP_IMAPS,
        "IRCS" : _consts.PORT_TCP_IRCS,
        "POP3S" : _consts.PORT_TCP_POP3S,
        "SOCKS" : _consts.PORT_TCP_SOCKS,
        "PROOFD" : _consts.PORT_TCP_PROOFD,
        "ROOTD" : _consts.PORT_TCP_ROOTD,
        "OPENVPN" : _consts.PORT_TCP_OPENVPN,
        "RMIREGISTRY" : _consts.PORT_TCP_RMIREGISTRY,
        "KAZAA" : _consts.PORT_TCP_KAZAA,
        "NESSUS" : _consts.PORT_TCP_NESSUS,
        "LOTUSNOTE" : _consts.PORT_TCP_LOTUSNOTE,
        "S" : _consts.PORT_TCP_S,
        "M" : _consts.PORT_TCP_M,
        "INGRESLOCK" : _consts.PORT_TCP_INGRESLOCK,
        "NP" : _consts.PORT_TCP_NP,
        "DATAMETRICS" : _consts.PORT_TCP_DATAMETRICS,
        "PORT" : _consts.PORT_TCP_PORT,
        "KERMIT" : _consts.PORT_TCP_KERMIT,
        "L2F" : _consts.PORT_TCP_L2F,
        "RADIUS" : _consts.PORT_TCP_RADIUS,
        "ACCT" : _consts.PORT_TCP_ACCT,
        "MSNP" : _consts.PORT_TCP_MSNP,
        "STATUS" : _consts.PORT_TCP_STATUS,
        "SERVER" : _consts.PORT_TCP_SERVER,
        "REMOTEPING" : _consts.PORT_TCP_REMOTEPING,
        "NFS" : _consts.PORT_TCP_NFS,
        "SC104" : _consts.PORT_TCP_SC104,
        "CVSPSERVER" : _consts.PORT_TCP_CVSPSERVER,
        "VENUS" : _consts.PORT_TCP_VENUS,
        "SE" : _consts.PORT_TCP_SE,
        "CODASRV" : _consts.PORT_TCP_CODASRV,
        "SE" : _consts.PORT_TCP_SE,
        "MON" : _consts.PORT_TCP_MON,
        "DICT" : _consts.PORT_TCP_DICT,
        "GPSD" : _consts.PORT_TCP_GPSD,
        "GDS_DB" : _consts.PORT_TCP_GDS_DB,
        "ICPV2" : _consts.PORT_TCP_ICPV2,
        "MYSQL" : _consts.PORT_TCP_MYSQL,
        "NUT" : _consts.PORT_TCP_NUT,
        "DISTCC" : _consts.PORT_TCP_DISTCC,
        "DAAP" : _consts.PORT_TCP_DAAP,
        "SVN" : _consts.PORT_TCP_SVN,
        "SUUCP" : _consts.PORT_TCP_SUUCP,
        "SYSRQD" : _consts.PORT_TCP_SYSRQD,
        "IAX" : _consts.PORT_TCP_IAX,
        "PORT" : _consts.PORT_TCP_PORT,
        "RFE" : _consts.PORT_TCP_RFE,
        "MMCC" : _consts.PORT_TCP_MMCC,
        "SIP" : _consts.PORT_TCP_SIP,
        "TLS" : _consts.PORT_TCP_TLS,
        "AOL" : _consts.PORT_TCP_AOL,
        "CLIENT" : _consts.PORT_TCP_CLIENT,
        "SERVER" : _consts.PORT_TCP_SERVER,
        "CFENGINE" : _consts.PORT_TCP_CFENGINE,
        "MDNS" : _consts.PORT_TCP_MDNS,
        "POSTGRESQL" : _consts.PORT_TCP_POSTGRESQL,
        "GGZ" : _consts.PORT_TCP_GGZ,
        "X11" : _consts.PORT_TCP_X11,
        "1" : _consts.PORT_TCP_1,
        "2" : _consts.PORT_TCP_2,
        "3" : _consts.PORT_TCP_3,
        "4" : _consts.PORT_TCP_4,
        "5" : _consts.PORT_TCP_5,
        "6" : _consts.PORT_TCP_6,
        "7" : _consts.PORT_TCP_7,
        "SVC" : _consts.PORT_TCP_SVC,
        "RTR" : _consts.PORT_TCP_RTR,
        "SGE_QMASTER" : _consts.PORT_TCP_SGE_QMASTER,
        "SGE_EXECD" : _consts.PORT_TCP_SGE_EXECD,
        "FILESERVER" : _consts.PORT_TCP_FILESERVER,
        "CALLBACK" : _consts.PORT_TCP_CALLBACK,
        "PRSERVER" : _consts.PORT_TCP_PRSERVER,
        "VLSERVER" : _consts.PORT_TCP_VLSERVER,
        "KASERVER" : _consts.PORT_TCP_KASERVER,
        "VOLSER" : _consts.PORT_TCP_VOLSER,
        "ERRORS" : _consts.PORT_TCP_ERRORS,
        "BOS" : _consts.PORT_TCP_BOS,
        "UPDATE" : _consts.PORT_TCP_UPDATE,
        "RMTSYS" : _consts.PORT_TCP_RMTSYS,
        "SERVICE" : _consts.PORT_TCP_SERVICE,
        "DIR" : _consts.PORT_TCP_DIR,
        "FD" : _consts.PORT_TCP_FD,
        "SD" : _consts.PORT_TCP_SD,
        "AMANDA" : _consts.PORT_TCP_AMANDA,
        "HKP" : _consts.PORT_TCP_HKP,
        "BPRD" : _consts.PORT_TCP_BPRD,
        "BPDBM" : _consts.PORT_TCP_BPDBM,
        "MSVC" : _consts.PORT_TCP_MSVC,
        "VNETD" : _consts.PORT_TCP_VNETD,
        "BPCD" : _consts.PORT_TCP_BPCD,
        "VOPIED" : _consts.PORT_TCP_VOPIED,
        "WNN6" : _consts.PORT_TCP_WNN6,
        "KERBEROS4" : _consts.PORT_TCP_KERBEROS4,
        "KERBEROS_MASTER" : _consts.PORT_TCP_KERBEROS_MASTER,
        "KRB_PROP" : _consts.PORT_TCP_KRB_PROP,
        "KRBUPDATE" : _consts.PORT_TCP_KRBUPDATE,
        "SWAT" : _consts.PORT_TCP_SWAT,
        "KPOP" : _consts.PORT_TCP_KPOP,
        "KNETD" : _consts.PORT_TCP_KNETD,
        "EKLOGIN" : _consts.PORT_TCP_EKLOGIN,
        "KX" : _consts.PORT_TCP_KX,
        "IPROP" : _consts.PORT_TCP_IPROP,
        "SUPFILESRV" : _consts.PORT_TCP_SUPFILESRV,
        "SUPFILEDBG" : _consts.PORT_TCP_SUPFILEDBG,
        "LINUXCONF" : _consts.PORT_TCP_LINUXCONF,
        "POPPASSD" : _consts.PORT_TCP_POPPASSD,
        "SSMTP" : _consts.PORT_TCP_SSMTP,
        "MOIRA_DB" : _consts.PORT_TCP_MOIRA_DB,
        "MOIRA_UPDATE" : _consts.PORT_TCP_MOIRA_UPDATE,
        "SPAMD" : _consts.PORT_TCP_SPAMD,
        "OMIRR" : _consts.PORT_TCP_OMIRR,
        "CUSTOMS" : _consts.PORT_TCP_CUSTOMS,
        "SKKSERV" : _consts.PORT_TCP_SKKSERV,
        "RMTCFG" : _consts.PORT_TCP_RMTCFG,
        "WIPLD" : _consts.PORT_TCP_WIPLD,
        "XTEL" : _consts.PORT_TCP_XTEL,
        "XTELW" : _consts.PORT_TCP_XTELW,
        "SUPPORT" : _consts.PORT_TCP_SUPPORT,
        "SIEVE" : _consts.PORT_TCP_SIEVE,
        "CFINGER" : _consts.PORT_TCP_CFINGER,
        "NDTP" : _consts.PORT_TCP_NDTP,
        "FROX" : _consts.PORT_TCP_FROX,
        "NINSTALL" : _consts.PORT_TCP_NINSTALL,
        "ZEBRASRV" : _consts.PORT_TCP_ZEBRASRV,
        "ZEBRA" : _consts.PORT_TCP_ZEBRA,
        "RIPD" : _consts.PORT_TCP_RIPD,
        "RIPNGD" : _consts.PORT_TCP_RIPNGD,
        "OSPFD" : _consts.PORT_TCP_OSPFD,
        "BGPD" : _consts.PORT_TCP_BGPD,
        "OSPF6D" : _consts.PORT_TCP_OSPF6D,
        "OSPFAPI" : _consts.PORT_TCP_OSPFAPI,
        "ISISD" : _consts.PORT_TCP_ISISD,
        "AFBACKUP" : _consts.PORT_TCP_AFBACKUP,
        "AFMBACKUP" : _consts.PORT_TCP_AFMBACKUP,
        "XTELL" : _consts.PORT_TCP_XTELL,
        "FAX" : _consts.PORT_TCP_FAX,
        "HYLAFAX" : _consts.PORT_TCP_HYLAFAX,
        "DISTMP3" : _consts.PORT_TCP_DISTMP3,
        "MUNIN" : _consts.PORT_TCP_MUNIN,
        "CSTATD" : _consts.PORT_TCP_CSTATD,
        "SSTATD" : _consts.PORT_TCP_SSTATD,
        "PCRD" : _consts.PORT_TCP_PCRD,
        "NOCLOG" : _consts.PORT_TCP_NOCLOG,
        "HOSTMON" : _consts.PORT_TCP_HOSTMON,
        "RPLAY" : _consts.PORT_TCP_RPLAY,
        "RPTP" : _consts.PORT_TCP_RPTP,
        "NSCA" : _consts.PORT_TCP_NSCA,
        "MRTD" : _consts.PORT_TCP_MRTD,
        "BGPSIM" : _consts.PORT_TCP_BGPSIM,
        "CANNA" : _consts.PORT_TCP_CANNA,
        "PORT" : _consts.PORT_TCP_PORT,
        "IRCD" : _consts.PORT_TCP_IRCD,
        "FTP" : _consts.PORT_TCP_FTP,
        "WEBCACHE" : _consts.PORT_TCP_WEBCACHE,
        "TPROXY" : _consts.PORT_TCP_TPROXY,
        "OMNIORB" : _consts.PORT_TCP_OMNIORB,
        "DAEMON" : _consts.PORT_TCP_DAEMON,
        "XINETD" : _consts.PORT_TCP_XINETD,
        "GIT" : _consts.PORT_TCP_GIT,
        "ZOPE" : _consts.PORT_TCP_ZOPE,
        "WEBMIN" : _consts.PORT_TCP_WEBMIN,
        "KAMANDA" : _consts.PORT_TCP_KAMANDA,
        "AMANDAIDX" : _consts.PORT_TCP_AMANDAIDX,
        "AMIDXTAPE" : _consts.PORT_TCP_AMIDXTAPE,
        "SMSQP" : _consts.PORT_TCP_SMSQP,
        "XPILOT" : _consts.PORT_TCP_XPILOT,
        "CAD" : _consts.PORT_TCP_CAD,
        "ISDNLOG" : _consts.PORT_TCP_ISDNLOG,
        "VBOXD" : _consts.PORT_TCP_VBOXD,
        "BINKP" : _consts.PORT_TCP_BINKP,
        "ASP" : _consts.PORT_TCP_ASP,
        "CSYNC2" : _consts.PORT_TCP_CSYNC2,
        "DIRCPROXY" : _consts.PORT_TCP_DIRCPROXY,
        "TFIDO" : _consts.PORT_TCP_TFIDO,
        "FIDO" : _consts.PORT_TCP_FIDO,
    }

class _HSequenceNumber(_fields.IntField):
    """
    The sequence number of the first data octet in this segment (except
    when SYN is present).

    See RFC 793 for more.
    """

    bits = 32
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class _HAcknowledgmentNumber(_fields.IntField):
    """
    If the ACK control bit is set this field contains the value of the
    next sequence number the sender of the segment is expecting to receive.

    See RFC 793 for more.
    """
    
    bits = 32
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 1

class _HDataOffset(_fields.SpecialIntField):
    """
    The number of 32 bit words in the TCP Header. This indicates where
    the data begins.

    See RFC 793 for more.
    """
    
    bits = 4
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # returns in 32-bits units
        return 5 + self._tmp_value / 32 # 5 is a minimum value

class _HReserved(_fields.IntField):
    """
    Reserved for future use.

    See RFC 793 for more.
    """
    
    bits = 6
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        return 0

class _HWindow(_fields.IntField):
    """
    The number of data octets beginning with the one indicated in the
    acknowledgment field which the sender of this segment is willing to accept.

    See RFC 793 for more.
    """
    
    bits = 16
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 512

class _HUrgentPointer(_fields.IntField):
    """
    This field communicates the current value of the urgent pointer as a
    positive offset from the sequence number in this segment.

    See RFC 793 for more.
    """
    
    bits = 16
    auto = True
    
    def _generate_value(self):
        """
        Generate value for undefined field yet.
        
        @return: auto-generated value of the field.
        """

        # TODO: implemention real auto-filling here ;)
        # otherwise we can simple return 0
        return 0

class TCP(_protocols.Protocol):
    """
    Transmission Control Protocol implementation.

    It the most common protocol in the Internet on fourth layer
    of the OSI model.
    """
    
    layer = 4       # layer of the OSI
    protocol_id = _consts.PROTOCOL_TCP
    name = "TCP"

    _ordered_fields = ('source_port', 'destination_port', '_sequence_number',
                    '_acknowledgment_number', '_data_offset', '_reserved',
                    'control_bits', '_window', '_checksum', '_urgent_pointer',
                    'options', '_padding',)

    def __init__(self, **kwargs):
        """
        Create a new TCP().
        """

        control_bits = ('urg', 'ack', 'psh', 'rst', 'syn', 'fin')
        control_bits_predefined = dict.fromkeys(control_bits, 0)

        fields_list = [ _HPort("Source Port", 0),
                        _HPort("Destination Port", 0),
                        _HSequenceNumber("Sequence Number"),
                        _HAcknowledgmentNumber("Acknowledgment Number"),
                        _HDataOffset("DataOffset"),
                        _HReserved("Reserved", 0),
                        _fields.Flags("Control Bits", control_bits,
                        **control_bits_predefined),
                        _HWindow("Window"),
                        _layer4.Layer4ChecksumField("Checksum"),
                        _HUrgentPointer("Urgent Pointer"),
                        _fields.Flags("Options", ()),
                        _fields.PaddingField("Padding") ]

        # we call super.__init__ after prepared necessary data
        super(TCP, self).__init__(fields_list, **kwargs)

        # set __doc__ for fields - it's important if you want to get hints
        # in some frontends. E.g. Umit Project provides one...
        self.get_field('source_port').set_doc("The source port number. "
            "See RFC 793 for more.")
        self.get_field('destination_port').set_doc("The destination port "
            "number. See RFC 793 for more.")
        self.get_field('control_bits').set_doc("URG, ACK, PSH, RST, SYN, FIN "
            "flags. See RFC 793 for more.")
        self.get_field('_checksum').set_doc("Checksum of Pseudo Header, TCP "
            "header and data. See RFC 793 for more.")
        self.get_field('options').set_doc("Options may occupy space at the "
            "end of the TCP header and are a multiple of 8 bits in length. "
            "See RFC 793 for more.")
        self.get_field('_padding').set_doc("The TCP header padding is used "
            "to ensure that the TCP header ends and data begins on a 32 bit "
            "boundary. See RFC 793 for more.")

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields before calling fillout() for them.

        Set Padding field and calculate header length.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        # Padding
        self.get_field('_padding')._tmp_value = \
                                                self.get_field('options').bits

        # Data Offset
        self.get_field('_data_offset')._tmp_value = \
            self.get_field('options').bits + self.get_field('_padding').bits

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        Handle with fields after calling fillout() for them.

        Calculate header checksum with new instance of PseudoHeader object.

        @type raw_value: C{int}
        @param raw_value: currently raw value for the packet.

        @type bit: C{int}
        @param bit: currently length of the protocol.

        @type protocol_container: C{tuple}
        @param protocol_container: tuple of protocols included in the packet.

        @type protocol_bits: C{int}
        @param protocol_bits: currently length of the packet.

        @return: C{raw_value, bit}
        """

        # rev_offset it the offset from the right side
        cksum_rev_offset = bit - self.get_offset('_checksum') - \
                                            self.get_field('_checksum').bits
        # checking if user not defined his own value of checksum
        if _bits.get_bits(raw_value, self.get_field('_checksum').bits,
                                    cksum_rev_offset, rev_offset=True) == 0:
            # Payload
            if self.payload:
                cksum = self.payload.__dict__['__raw_value']
            else:
                cksum = 0
            offset = protocol_bits

            # TCP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # TCP header length...converted to bits unit
            total_length = self.get_field('_data_offset').fillout()*32
            # add payload
            total_length += protocol_bits
            # conversion to bytes unit
            total_length /= 8

            # create pseudo header object
            pheader = _layer4.PseudoHeader(self.protocol_id, total_length)
            # generate raw value of it
            pheader_raw = pheader.get_raw(protocol_container, protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_raw << offset

            # finally, calcute and apply checksum
            raw_cksum = _net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_rev_offset

        return raw_value, bit

protocols = [ TCP, ]
