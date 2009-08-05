==========
 Sniffing
==========


Introduction
============

Since v0.2 UMPA provides a new feature to capture packets over the network.
It uses well known libpcap[1] as a background and users who are familiar
with it can easily understand and use UMPA's sniffing tool.

.. note::

    using libpcap requires root privileges!

The First Step
==============

``umit.umpa.sniffing`` provides the following functions for sniffing:
 1. sniff()
 2. sniff_next()
 3. sniff_any()
 4. sniff_loop()
 5. to_file()
 6. from_file()
 7. from_file_loop()

The main function is obviously ``sniff()`` and the rest of them simple wrap
this function to make our life easier. Also, most of arguments for all of these
functions are the same and keep in the same order (for some functions
like \*_loop() additional arguments were added at the end).
Functions 2-3 are very similar to the first one and in this paragraph we gonna
focus on these 3 functions.

Basically, the simplest function is ``sniff_any()``, you can call it and
you will get a first arrived packet from the network. That's all. You can't set
anything (apart from store it on your harddrive).

In contrary to ``sniff_any()``, ``sniff()`` gives you full control on sniffing
packets. You can set how many packets you expect, filter packets,
select network interface and many more. For details, please check pydocs
of ``umit.umpa.sniffing`` package. In libpcap's manuals you can find
interesting informations as well.

Lets imagine the following situation. We need first 3 packets sent to us on our
port 80. Just to see what's goin on. Our IP in this case is ``127.0.0.1``.
And we are interested in loopback interface

.. code-block:: python

    In [1]: from umit.umpa.sniffing import sniff
    In [2]: packets = umit.umpa.sniffing.sniff(10, filter="src host 127.0.0.1 and port 80", device="lo")

    In [3]: len(packets)
    Out[3]: 3

    In [4]: for pkt in packets:
       ...:     print pkt
    Packet contains 4 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa14c2cc>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 60
    | +-[ Identification            ]	_id             : 38286
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 42795
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa14c3cc>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 40551
    | +-[ Destination Port          ]	dstport         : 80
    | +-[ Sequence Number           ]	_seq            : 4002535750
    | +-[ Acknowledgment Number     ]	_ack            : 4004130011
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	1
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 513
    | +-[ Checksum                  ]	_checksum       : 65072
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899079550965555890515
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa14c08c>
    +-< Payload                     >
    | \
    | +-[ Data                      ]	data            : this is

    \-< Payload                     >	contains 1 fields
    <umit.umpa.protocols.Payload.Payload object at 0xa14c2ec>
    <umit.umpa._packets.Packet object at 0xa14c5cc>
    Packet contains 3 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa14caac>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 52
    | +-[ Identification            ]	_id             : 24866
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 56223
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa14c82c>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 80
    | +-[ Destination Port          ]	dstport         : 40551
    | +-[ Sequence Number           ]	_seq            : 4004130011
    | +-[ Acknowledgment Number     ]	_ack            : 4002535758
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	0
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 512
    | +-[ Checksum                  ]	_checksum       : 52183
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899079550965555893207
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa14c6cc>
    <umit.umpa._packets.Packet object at 0xa14c54c>
    Packet contains 4 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa14ce0c>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 62
    | +-[ Identification            ]	_id             : 38287
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 42792
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa14cf4c>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 40551
    | +-[ Destination Port          ]	dstport         : 80
    | +-[ Sequence Number           ]	_seq            : 4002535758
    | +-[ Acknowledgment Number     ]	_ack            : 4004130011
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	1
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 513
    | +-[ Checksum                  ]	_checksum       : 65074
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899079553100154639319
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa1512ec>
    +-< Payload                     >
    | \
    | +-[ Data                      ]	data            : umpa umpa

    \-< Payload                     >	contains 1 fields
    <umit.umpa.protocols.Payload.Payload object at 0xa14cdac>
    <umit.umpa._packets.Packet object at 0xa14c9cc>

As you can see, we got 3 packets (``umit.umpa.Packet``'s objects). 2 sent to
a port 80 and 1 packet from the port 80.
If we are intrestested to get just 1 packet, we can also use ``sniff_next()``
which is equivalent to pass ``1`` as a first argument in ``sniff()``.


Callbacks
=========

By using callbacks we can simple register functions which will be called when
suitable packet will be sniffed. These functions are ending with ''_loop'' word
in the func name.

Before we will register a callback function, we have define it. It has fixed
arguments list: ``timestamp, pkt, *callback_args``.

.. code-block:: python

    def callback_func(timestamp, pkt, *args):
        print "[%f] Captured a new packet.." % timestamp
        print pkt
        print

The callback's function simple print a timestamp in brackets with a notification
and after that, print sniffed packet. Let's register this function.

.. code-block:: python

    In [5]: umit.umpa.sniffing.sniff_loop(3, callback=callback, filter="src host 127.0.0.1 and port 80", device="lo")
    [1249423424.454845] Captured a new packet..
    Packet contains 4 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa1574ec>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 61
    | +-[ Identification            ]	_id             : 38289
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 42791
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa15716c>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 40551
    | +-[ Destination Port          ]	dstport         : 80
    | +-[ Sequence Number           ]	_seq            : 4002535777
    | +-[ Acknowledgment Number     ]	_ack            : 4004130011
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	1
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 513
    | +-[ Checksum                  ]	_checksum       : 65073
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899081384963836337783
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa1573ec>
    +-< Payload                     >
    | \
    | +-[ Data                      ]	data            : callback

    \-< Payload                     >	contains 1 fields
    <umit.umpa.protocols.Payload.Payload object at 0xa15778c>
    <umit.umpa._packets.Packet object at 0xa14ca2c>

    [1249423424.454873] Captured a new packet..
    Packet contains 3 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa15794c>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 52
    | +-[ Identification            ]	_id             : 24869
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 56220
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa1579ec>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 80
    | +-[ Destination Port          ]	dstport         : 40551
    | +-[ Sequence Number           ]	_seq            : 4004130011
    | +-[ Acknowledgment Number     ]	_ack            : 4002535786
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	0
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 512
    | +-[ Checksum                  ]	_checksum       : 50088
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899081384963836352474
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa157cec>
    <umit.umpa._packets.Packet object at 0xa15132c>

    [1249423429.719059] Captured a new packet..
    Packet contains 4 protocols
    +-< Ethernet                    >
    | \
    | +-[ Destination               ]	dst             : 00:00:00:00:00:00
    | +-[ Source                    ]	src             : 00:00:00:00:00:00
    | +-[ Type                      ]	_type           : 2048
    \-< Ethernet                    >	contains 3 fields
    <umit.umpa.protocols.Ethernet.Ethernet object at 0xa1574ec>
    +-< IP                          >
    | \
    | +-[ Version                   ]	_version        : 4
    | +-[ IHL                       ]	_hdr_len        : 5
    | +-[ TOS                       ]	tos
    | | \
    | |  -{ precedence0             }	0
    | |  -{ precedence1             }	0
    | |  -{ precedence2             }	0
    | |  -{ delay                   }	0
    | |  -{ throughput              }	0
    | |  -{ reliability             }	0
    | |  -{ reserved0               }	0
    | |  -{ reserved1               }	0
    | | /
    | \-[ TOS                       ]	contains 8 bit flags
    | +-[ Total Length              ]	_len            : 62
    | +-[ Identification            ]	_id             : 38290
    | +-[ Flags                     ]	flags
    | | \
    | |  -{ rb                      }	0
    | |  -{ df                      }	1
    | |  -{ mf                      }	0
    | | /
    | \-[ Flags                     ]	contains 3 bit flags
    | +-[ Fragment Offset           ]	_frag_offset    : 0
    | +-[ TTL                       ]	ttl             : 64
    | +-[ Protocol                  ]	_proto          : 6
    | +-[ Header Checksum           ]	_checksum       : 42789
    | +-[ Source Address            ]	src             : 127.0.0.1
    | +-[ Destination Address       ]	dst             : 127.0.0.1
    | +-[ Options                   ]	options         : 0
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< IP                          >	contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xa15758c>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]	srcport         : 40551
    | +-[ Destination Port          ]	dstport         : 80
    | +-[ Sequence Number           ]	_seq            : 4002535786
    | +-[ Acknowledgment Number     ]	_ack            : 4004130011
    | +-[ Data Offset               ]	_hdr_len        : 8
    | +-[ Reserved                  ]	_reserved       : 0
    | +-[ Control Bits              ]	flags
    | | \
    | |  -{ urg                     }	0
    | |  -{ ack                     }	1
    | |  -{ psh                     }	1
    | |  -{ rst                     }	0
    | |  -{ syn                     }	0
    | |  -{ fin                     }	0
    | | /
    | \-[ Control Bits              ]	contains 6 bit flags
    | +-[ Window                    ]	_window_size    : 513
    | +-[ Checksum                  ]	_checksum       : 65074
    | +-[ Urgent Pointer            ]	_urgent_pointer : 0
    | +-[ Options                   ]	options         : 310731899081390616013314010
    | +-[ Padding                   ]	_padding        : 0 (auto - 0)
    \-< TCP                         >	contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xa1576cc>
    +-< Payload                     >
    | \
    | +-[ Data                      ]	data            : umpa umpa

    \-< Payload                     >	contains 1 fields
    <umit.umpa.protocols.Payload.Payload object at 0xa1578ec>
    <umit.umpa._packets.Packet object at 0xa14ca2c>


Dealing with files
==================

We can also read packets from files or store results there.
Let's store packet to file first and then load them.

There are 2 options to store packets on our harddrive. We can use special
function ``to_file()`` or use special argument for any sniff*() functions
called ''dump''. The difference is only that using sniff* functions we can
still do other things with already sniffed packets and storing packets is
just an option. ``to_file()`` is focused only on storing packets.

It's pretty simple and there is no need more explanation.
Just show on the example below.

.. code-block:: python

    In [6]: umit.umpa.sniffing.to_file('/tmp/our_packets.cap', 3, "src host 127.0.0.1 and port 80", "lo")

As you can notice, we used .cap extensions. And yes, our packets can be read
by any application which is able to read .cap format's files (e.g. wireshark).

Now, let's read packets back. We have to use one of the functions:
``from_file()`` or ``from_file_loop()``. A distinction between them is about
callback what is already explained above.

.. code-block:: python

    In [7]: packets = umit.umpa.sniffing.from_file('/tmp/our_packets.cap')

We can use filter, count or other arguments as well to limit loaded packets.
But in this case we wanna load everything from a file.
