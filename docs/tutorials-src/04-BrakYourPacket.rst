===================
 Break Your Packet
===================


Introduction
============

UMPA can build a lot of different packets - exactly as you wish. Usually,
you expect that packets will be proper, but sometimes you wish to get broken
packets. If you really wish - this tutorial is for you!

You will learn how to send completely odd packets like IP packet as a payload
of TCP packet or with broken bits.


Usecases
--------

 * testing hardware (resistance tests)
 * testing kernel


The strict option
=================

Let's say we would like to build a packet where TCP header is before IP header.

.. code-block:: python

    import umit.umpa
    from umit.umpa.protocols import IP, TCP

    ip = IP(source_address="127.0.0.1", destination_address="67.205.14.183")
    tcp = TCP(source_port=2958, destination_port=0)

In the normal case UMPA will raise UMPAStrictException.

.. code-block:: python

    In [5]: packet = umit.umpa.Packet(tcp, ip)
    ---------------------------------------------------------------------------
    <class 'umit.umpa.utils.exceptions.UMPAStrictException'>Traceback (most recent call last)

    /home/xsx/UMPA/<ipython console> in <module>()

    /home/xsx/UMPA/umit/umpa/_packets.py in __init__(self, *protos, **options)
         95 
         96         self.protos = []
    ---> 97         self._add_new_protocols(protos)
         98         self.raw = None
         99         self.bits = 0

    /home/xsx/UMPA/umit/umpa/_packets.py in _add_new_protocols(self, protos)
        142                         raise UMPAStrictException("bad protocols ordering."
        143                             "first layer %d, second %d."
    --> 144                             % (last_proto.layer, proto.layer))
        145                     else:
        146                         _strict_warn(last_proto.layer, proto.layer)

    <class 'umit.umpa.utils.exceptions.UMPAStrictException'>: 'bad protocols ordering. first layer 4, second 3.'

    In [6]: 

We can avoid this by ``strict`` option.

.. code-block:: python

    In [6]: packet = umit.umpa.Packet(tcp, ip, strict=False)
    umit/umpa/_packets.py:97: StrictWarning: bad protocols ordering. first layer 4, second 3.
      self._add_new_protocols(protos)

    In [7]: 

We got the warning but the packet is built. Also we can silence warnings
by ``warn`` option if needed.

.. code-block:: python

    In [7]: packet = umit.umpa.Packet(tcp, ip, strict=False, warn=False)

    In [8]: 

Also, both options can be set later for the object:

.. code-block:: python

    In [8]: packet = umit.umpa.Packet()

    In [9]: packet.warn = False

    In [10]: packet.strict = True

    In [11]: 


Broken bits
===========

If we want to break just some bits, it's completely easy. Let's say, we want
to set broken header checksum field for UDP.

.. code-block:: python

    import umit.umpa.protocols

    udp = umit.umpa.protocols.UDP(destination_port=0, source_port=0)
    udp._checksum = 0xffff

The UDP's checksum field has set 0xffff value and UMPA will not generate correct value.
