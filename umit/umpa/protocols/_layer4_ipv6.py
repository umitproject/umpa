#!/usr/bin/env python

"""
Usefull classes for 4th layer's protocols.

TCP/UDP use special pseudo header to calculate checksum. These classes
are provided.
"""

from umit.umpa.protocols._protocols import Protocol
from umit.umpa.protocols.IPV6 import IPV6
from umit.umpa.protocols._fields import IntField, IPv4AddrField, IPv6AddrField

class Layer4ChecksumField(IntField):
    """
    """

    bits = 16
    auto = True

    def _generate_value(self):
        """
        """

        return 0

class PseudoHeader(Protocol):
    """
    """

    _ordered_fields = ('src', 'dst', 'reserved',
                    'protocol_id', 'total_length')

    def __init__(self, protocol_id, total_length):
        """
        """
		
        fields_list = [ IPv6AddrField("Source Address"),
                        IPv6AddrField("Destination Address"),
                        IntField("Reserved", 0, bits=8),
                        IntField("Protocol", protocol_id, bits=8),
                        IntField("Total Length", total_length, bits=16) ]
        super(PseudoHeader, self).__init__(fields_list)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        """

        # assign localhost first becuase if there is none IP instance
        self.src = "0:0:0:0:0:0:0:1"
        self.dst = "0:0:0:0:0:0:0:1"
        # grabbing informations from the IP's header
        it = iter(protocol_container)
        for proto in it:
            if isinstance(proto, IPV6):
                self.src = proto.src
                self.dst = proto.dst
                break

        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        """

        return raw_value, bit
