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

    _ordered_fields = ('src', 'dst', 'uplaylen',
                    'zero', 'protocol')

    def __init__(self, protocol_id, total_length):
        """
        """
        print "=================::::::::::::::::::::::"
        print total_length
        print protocol_id
		
        fields_list = [ IPv6AddrField("Source Address"),
                        IPv6AddrField("Destination Address"),
                        IntField("Upper layer length", total_length, bits=32),
                        IntField("zero", 0, bits=24),
                        IntField("Next Header ", protocol_id , bits=8) ]
        super(PseudoHeader, self).__init__(fields_list)

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        """
        """

        # assign localhost first becuase if there is none IP instance
        self.src = "0000:0000:0000:0000:0000:0000:0000:0001"
        self.dst = "0000:0000:0000:0000:0000:0000:0000:0001"
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
