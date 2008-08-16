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

from umpa.protocols import _consts
from umpa.protocols import _fields
from umpa.protocols import _protocols
from umpa.protocols import _layer4
from umpa.utils import net
from umpa.utils import bits

class _HPort(_fields.EnumField):
    bits = 16
    auto = False
    enumerable = {
        "ECHO" : _consts.PORT_UDP_ECHO,
        "DISCARD" : _consts.PORT_UDP_DISCARD,
        "DAYTIME" : _consts.PORT_UDP_DAYTIME,
        "MSP" : _consts.PORT_UDP_MSP,
        "CHARGEN" : _consts.PORT_UDP_CHARGEN,
        "FSP" : _consts.PORT_UDP_FSP,
        "SSH" : _consts.PORT_UDP_SSH,
        "TIME" : _consts.PORT_UDP_TIME,
        "RLP" : _consts.PORT_UDP_RLP,
        "TACACS" : _consts.PORT_UDP_TACACS,
        "CK" : _consts.PORT_UDP_CK,
        "DOMAIN" : _consts.PORT_UDP_DOMAIN,
        "DS" : _consts.PORT_UDP_DS,
        "BOOTPS" : _consts.PORT_UDP_BOOTPS,
        "BOOTPC" : _consts.PORT_UDP_BOOTPC,
        "TFTP" : _consts.PORT_UDP_TFTP,
        "GOPHER" : _consts.PORT_UDP_GOPHER,
        "WWW" : _consts.PORT_UDP_WWW,
        "KERBEROS" : _consts.PORT_UDP_KERBEROS,
        "NEMA" : _consts.PORT_UDP_NEMA,
        "NS" : _consts.PORT_UDP_NS,
        "RTELNET" : _consts.PORT_UDP_RTELNET,
        "POP2" : _consts.PORT_UDP_POP2,
        "POP3" : _consts.PORT_UDP_POP3,
        "SUNRPC" : _consts.PORT_UDP_SUNRPC,
        "NTP" : _consts.PORT_UDP_NTP,
        "PWDGEN" : _consts.PORT_UDP_PWDGEN,
        "SRV" : _consts.PORT_UDP_SRV,
        "NS" : _consts.PORT_UDP_NS,
        "DGM" : _consts.PORT_UDP_DGM,
        "SSN" : _consts.PORT_UDP_SSN,
        "IMAP2" : _consts.PORT_UDP_IMAP2,
        "SNMP" : _consts.PORT_UDP_SNMP,
        "TRAP" : _consts.PORT_UDP_TRAP,
        "MAN" : _consts.PORT_UDP_MAN,
        "AGENT" : _consts.PORT_UDP_AGENT,
        "MAILQ" : _consts.PORT_UDP_MAILQ,
        "XDMCP" : _consts.PORT_UDP_XDMCP,
        "NEXTSTEP" : _consts.PORT_UDP_NEXTSTEP,
        "BGP" : _consts.PORT_UDP_BGP,
        "PROSPERO" : _consts.PORT_UDP_PROSPERO,
        "IRC" : _consts.PORT_UDP_IRC,
        "SMUX" : _consts.PORT_UDP_SMUX,
        "RTMP" : _consts.PORT_UDP_RTMP,
        "NBP" : _consts.PORT_UDP_NBP,
        "ECHO" : _consts.PORT_UDP_ECHO,
        "ZIS" : _consts.PORT_UDP_ZIS,
        "QMTP" : _consts.PORT_UDP_QMTP,
        "Z3950" : _consts.PORT_UDP_Z3950,
        "IPX" : _consts.PORT_UDP_IPX,
        "IMAP3" : _consts.PORT_UDP_IMAP3,
        "PAWSERV" : _consts.PORT_UDP_PAWSERV,
        "ZSERV" : _consts.PORT_UDP_ZSERV,
        "FATSERV" : _consts.PORT_UDP_FATSERV,
        "RPC2PORTMAP" : _consts.PORT_UDP_RPC2PORTMAP,
        "CODAAUTH2" : _consts.PORT_UDP_CODAAUTH2,
        "CLEARCASE" : _consts.PORT_UDP_CLEARCASE,
        "ULISTSERV" : _consts.PORT_UDP_ULISTSERV,
        "LDAP" : _consts.PORT_UDP_LDAP,
        "IMSP" : _consts.PORT_UDP_IMSP,
        "HTTPS" : _consts.PORT_UDP_HTTPS,
        "SNPP" : _consts.PORT_UDP_SNPP,
        "DS" : _consts.PORT_UDP_DS,
        "KPASSWD" : _consts.PORT_UDP_KPASSWD,
        "SAFT" : _consts.PORT_UDP_SAFT,
        "ISAKMP" : _consts.PORT_UDP_ISAKMP,
        "RTSP" : _consts.PORT_UDP_RTSP,
        "NQS" : _consts.PORT_UDP_NQS,
        "LOCAL" : _consts.PORT_UDP_LOCAL,
        "GUI" : _consts.PORT_UDP_GUI,
        "IND" : _consts.PORT_UDP_IND,
        "IPP" : _consts.PORT_UDP_IPP,
        "BIFF" : _consts.PORT_UDP_BIFF,
        "WHO" : _consts.PORT_UDP_WHO,
        "SYSLOG" : _consts.PORT_UDP_SYSLOG,
        "TALK" : _consts.PORT_UDP_TALK,
        "NTALK" : _consts.PORT_UDP_NTALK,
        "ROUTE" : _consts.PORT_UDP_ROUTE,
        "TIMED" : _consts.PORT_UDP_TIMED,
        "NETWALL" : _consts.PORT_UDP_NETWALL,
        "GDOMAP" : _consts.PORT_UDP_GDOMAP,
        "AFPOVERTCP" : _consts.PORT_UDP_AFPOVERTCP,
        "NNTPS" : _consts.PORT_UDP_NNTPS,
        "SUBMISSION" : _consts.PORT_UDP_SUBMISSION,
        "LDAPS" : _consts.PORT_UDP_LDAPS,
        "TINC" : _consts.PORT_UDP_TINC,
        "SILC" : _consts.PORT_UDP_SILC,
        "WEBSTER" : _consts.PORT_UDP_WEBSTER,
        "RSYNC" : _consts.PORT_UDP_RSYNC,
        "TELNETS" : _consts.PORT_UDP_TELNETS,
        "IMAPS" : _consts.PORT_UDP_IMAPS,
        "IRCS" : _consts.PORT_UDP_IRCS,
        "POP3S" : _consts.PORT_UDP_POP3S,
        "SOCKS" : _consts.PORT_UDP_SOCKS,
        "PROOFD" : _consts.PORT_UDP_PROOFD,
        "ROOTD" : _consts.PORT_UDP_ROOTD,
        "OPENVPN" : _consts.PORT_UDP_OPENVPN,
        "RMIREGISTRY" : _consts.PORT_UDP_RMIREGISTRY,
        "KAZAA" : _consts.PORT_UDP_KAZAA,
        "NESSUS" : _consts.PORT_UDP_NESSUS,
        "LOTUSNOTE" : _consts.PORT_UDP_LOTUSNOTE,
        "S" : _consts.PORT_UDP_S,
        "M" : _consts.PORT_UDP_M,
        "INGRESLOCK" : _consts.PORT_UDP_INGRESLOCK,
        "NP" : _consts.PORT_UDP_NP,
        "DATAMETRICS" : _consts.PORT_UDP_DATAMETRICS,
        "PORT" : _consts.PORT_UDP_PORT,
        "KERMIT" : _consts.PORT_UDP_KERMIT,
        "L2F" : _consts.PORT_UDP_L2F,
        "RADIUS" : _consts.PORT_UDP_RADIUS,
        "ACCT" : _consts.PORT_UDP_ACCT,
        "MSNP" : _consts.PORT_UDP_MSNP,
        "NFS" : _consts.PORT_UDP_NFS,
        "SC104" : _consts.PORT_UDP_SC104,
        "CVSPSERVER" : _consts.PORT_UDP_CVSPSERVER,
        "VENUS" : _consts.PORT_UDP_VENUS,
        "SE" : _consts.PORT_UDP_SE,
        "CODASRV" : _consts.PORT_UDP_CODASRV,
        "SE" : _consts.PORT_UDP_SE,
        "MON" : _consts.PORT_UDP_MON,
        "DICT" : _consts.PORT_UDP_DICT,
        "GPSD" : _consts.PORT_UDP_GPSD,
        "GDS_DB" : _consts.PORT_UDP_GDS_DB,
        "ICPV2" : _consts.PORT_UDP_ICPV2,
        "MYSQL" : _consts.PORT_UDP_MYSQL,
        "NUT" : _consts.PORT_UDP_NUT,
        "DISTCC" : _consts.PORT_UDP_DISTCC,
        "DAAP" : _consts.PORT_UDP_DAAP,
        "SVN" : _consts.PORT_UDP_SVN,
        "SUUCP" : _consts.PORT_UDP_SUUCP,
        "SYSRQD" : _consts.PORT_UDP_SYSRQD,
        "IAX" : _consts.PORT_UDP_IAX,
        "PORT" : _consts.PORT_UDP_PORT,
        "RFE" : _consts.PORT_UDP_RFE,
        "MMCC" : _consts.PORT_UDP_MMCC,
        "SIP" : _consts.PORT_UDP_SIP,
        "TLS" : _consts.PORT_UDP_TLS,
        "AOL" : _consts.PORT_UDP_AOL,
        "CLIENT" : _consts.PORT_UDP_CLIENT,
        "SERVER" : _consts.PORT_UDP_SERVER,
        "CFENGINE" : _consts.PORT_UDP_CFENGINE,
        "MDNS" : _consts.PORT_UDP_MDNS,
        "POSTGRESQL" : _consts.PORT_UDP_POSTGRESQL,
        "GGZ" : _consts.PORT_UDP_GGZ,
        "X11" : _consts.PORT_UDP_X11,
        "1" : _consts.PORT_UDP_1,
        "2" : _consts.PORT_UDP_2,
        "3" : _consts.PORT_UDP_3,
        "4" : _consts.PORT_UDP_4,
        "5" : _consts.PORT_UDP_5,
        "6" : _consts.PORT_UDP_6,
        "7" : _consts.PORT_UDP_7,
        "SVC" : _consts.PORT_UDP_SVC,
        "RTR" : _consts.PORT_UDP_RTR,
        "SGE_QMASTER" : _consts.PORT_UDP_SGE_QMASTER,
        "SGE_EXECD" : _consts.PORT_UDP_SGE_EXECD,
        "FILESERVER" : _consts.PORT_UDP_FILESERVER,
        "CALLBACK" : _consts.PORT_UDP_CALLBACK,
        "PRSERVER" : _consts.PORT_UDP_PRSERVER,
        "VLSERVER" : _consts.PORT_UDP_VLSERVER,
        "KASERVER" : _consts.PORT_UDP_KASERVER,
        "VOLSER" : _consts.PORT_UDP_VOLSER,
        "ERRORS" : _consts.PORT_UDP_ERRORS,
        "BOS" : _consts.PORT_UDP_BOS,
        "UPDATE" : _consts.PORT_UDP_UPDATE,
        "RMTSYS" : _consts.PORT_UDP_RMTSYS,
        "SERVICE" : _consts.PORT_UDP_SERVICE,
        "DIR" : _consts.PORT_UDP_DIR,
        "FD" : _consts.PORT_UDP_FD,
        "SD" : _consts.PORT_UDP_SD,
        "AMANDA" : _consts.PORT_UDP_AMANDA,
        "HKP" : _consts.PORT_UDP_HKP,
        "BPRD" : _consts.PORT_UDP_BPRD,
        "BPDBM" : _consts.PORT_UDP_BPDBM,
        "MSVC" : _consts.PORT_UDP_MSVC,
        "VNETD" : _consts.PORT_UDP_VNETD,
        "BPCD" : _consts.PORT_UDP_BPCD,
        "VOPIED" : _consts.PORT_UDP_VOPIED,
        "WNN6" : _consts.PORT_UDP_WNN6,
        "KERBEROS4" : _consts.PORT_UDP_KERBEROS4,
        "KERBEROS_MASTER" : _consts.PORT_UDP_KERBEROS_MASTER,
        "PASSWD_SERVER" : _consts.PORT_UDP_PASSWD_SERVER,
        "SRV" : _consts.PORT_UDP_SRV,
        "CLT" : _consts.PORT_UDP_CLT,
        "HM" : _consts.PORT_UDP_HM,
        "POPPASSD" : _consts.PORT_UDP_POPPASSD,
        "MOIRA_UREG" : _consts.PORT_UDP_MOIRA_UREG,
        "OMIRR" : _consts.PORT_UDP_OMIRR,
        "CUSTOMS" : _consts.PORT_UDP_CUSTOMS,
        "PREDICT" : _consts.PORT_UDP_PREDICT,
        "NINSTALL" : _consts.PORT_UDP_NINSTALL,
        "AFBACKUP" : _consts.PORT_UDP_AFBACKUP,
        "AFMBACKUP" : _consts.PORT_UDP_AFMBACKUP,
        "NOCLOG" : _consts.PORT_UDP_NOCLOG,
        "HOSTMON" : _consts.PORT_UDP_HOSTMON,
        "RPLAY" : _consts.PORT_UDP_RPLAY,
        "RPTP" : _consts.PORT_UDP_RPTP,
        "OMNIORB" : _consts.PORT_UDP_OMNIORB,
        "MANDELSPAWN" : _consts.PORT_UDP_MANDELSPAWN,
        "KAMANDA" : _consts.PORT_UDP_KAMANDA,
        "SMSQP" : _consts.PORT_UDP_SMSQP,
        "XPILOT" : _consts.PORT_UDP_XPILOT,
        "CMSD" : _consts.PORT_UDP_CMSD,
        "CRSD" : _consts.PORT_UDP_CRSD,
        "GCD" : _consts.PORT_UDP_GCD,
        "ISDNLOG" : _consts.PORT_UDP_ISDNLOG,
        "VBOXD" : _consts.PORT_UDP_VBOXD,
        "ASP" : _consts.PORT_UDP_ASP
    }

class _HLength(_fields.SpecialIntField):
    """Length  is the length  in octets  of this user datagram  including  this
    header  and the data.
    """
    bits = 16
    auto = True
    def _generate_value(self):
        # returns in byte units
        return 8 + self._tmp_value/8    # minimum is 8

class UDP(_protocols.Protocol):
    """This is User Datagram Protocol.
    
    This protocol  provides  a procedure  for application  programs  to send
    messages  to other programs  with a minimum  of protocol mechanism.  The
    protocol  is transaction oriented, and delivery and duplicate protection
    are not guaranteed.
    """
    layer = 4
    protocol_id = _consts.PROTOCOL_UDP
    name = "UDP"

    _ordered_fields = ('source_port', 'destination_port', '_length',
                                                            '_checksum')

    def __init__(self, **kw):
        fields_list = [ _HPort("Source Port", 0),
                        _HPort("Destination Port", 0),
                        _HLength("Length"),
                        _layer4.Layer4ChecksumField("Checksum"), ]

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
                cksum = self.payload.__dict__['__raw_value']
            else:
                cksum = 0
            offset = protocol_bits

            # UDP Header
            cksum |= raw_value << offset
            offset += bit

            # Pseudo Header
            #
            # create pseudo header object
            pheader = _layer4.PseudoHeader(self.protocol_id,
                                        self._get_field('_length').fillout())
            # generate raw value of it
            pheader_raw = pheader._get_raw(protocol_container,
                                                        protocol_bits)[0]
            # added pseudo header bits to cksum value
            cksum |= pheader_raw << offset

            # finally, calcute and apply checksum
            raw_cksum = net.in_cksum(cksum)
            raw_value |= raw_cksum << cksum_rev_offset

        return raw_value, bit

protocols = [ UDP, ]
__all__ = [ "UDP", ]
