====================
 Your First Packets
====================

Introduction 
============

This tutorial is meant for everybody who wants to start using UMPA.
You will learn how to build and send your packets.

Examples
--------

Check examples/* directory for already written full code examples.

They are also available on http://trac.umitproject.org/browser/branch/UMPA/examples/

..2, 3...GO!
============


import UMPA
-----------

Ok, at the beginning we need to import UMPA.

.. code-block:: python

    In [1]: import umit.umpa
    In [2]:

Pretty easy, isn't it? ;-)

After that, we have 2 classes provided: ``Packet`` and ``Socket``.
The former one is a protocol container. If you want to build new packet,
you have to create a Packet's object. We will use it everytime when we would
like to build packets.

``Socket`` is needed at the end of the process. We will back
to this point later.


security issue
--------------

To create RAW_SOCKET we need SUID (root priviliges), but for normal usage
usually it's not necessary (depends what you are doing with your application).

So, it's recommended to drop the priviliges and up them only if needed.
``umit.umpa.utils`` package provides some useful modules, and
the ``umit.umpa.utils.security`` module provides functions which are usefull
in this case.

All we need is to import the module and call the function. Later when we need
to create a new socket (or to do something other what rely on SUID) we call
another function from the module (it will be describe later).

.. code-block:: python

    In [2]: import umit.umpa.utils.security
    In [3]: umit.umpa.utils.security.drop_priviliges()
    In [4]: 

Please note that our process has to be run as a root. Otherwise, an excaption
will raise:

.. code-block:: python

    In [1]: import umit.umpa.utils.security
    In [2]: umit.umpa.utils.security.drop_priviliges()

    Run the program with root-priviliges.

    ---------------------------------------------------------------------------
    <type 'exceptions.OSError'>               Traceback (most recent call last)

    /home/xsx/UMPA/<ipython console> in <module>()

    /home/xsx/UMPA/umpa/utils/security.py in drop_priviliges()
         48     nobody_id = pwd.getpwnam('nobody')[2]
         49     try:
    ---> 50         os.seteuid(nobody_id)
         51     except OSError:
         52         print >> sys.stderr, "Run the program with root-priviliges.\n"

    <type 'exceptions.OSError'>: [Errno 1] Operation not permitted

    In [3]: 


protocols
---------

Let's build our first packet. There are several ways to do that. We can include
each protocols as an arguments in ``Packet()`` constructor, or just build
them independent. The second case is more interesting.

First, we need to import the ``umit.umpa.protocols`` package. If we don't know
which protocols are available, we can simple check it.

.. code-block:: python

    In [4]: import umit.umpa.protocols

    In [5]: umit.umpa.protocols.get_all()
    Out[5]: 
    {'IP': <class 'umit.umpa.protocols.IP.IP'>,
     'Payload': <class 'umit.umpa.protocols.Payload.Payload'>,
     'TCP': <class 'umit.umpa.protocols.TCP.TCP'>,
     'UDP': <class 'umit.umpa.protocols.UDP.UDP'>}
     
    In [6]:

There are two more functions (``get_globals()`` and ``get_locals()``). We will
talk about them in next tutorials. But ``get_all()`` is what you usually need.

OK, in our example we would like to build TCP/IP packet and UDP/IP.
Both packets with the same IP header.


IP protocol
-----------

.. code-block:: python

    In [6]: ip = umit.umpa.protocols.IP(source_address="127.0.0.1")

    In [7]: ip.destination_address = (67,205,14,183)

    In [8]: list(ip.get_fields_keys())
    Out[8]: 
    ['_version',
     '_ihl',
     'type_of_service',
     '_total_length',
     '_identification',
     'flags',
     '_fragment_offset',
     'time_to_live',
     '_protocol',
     '_header_checksum',
     'source_address',
     'destination_address',
     'options',
     '_padding']

Ok, We've just created the IP instance. As you see, we can pass values directly
to constructor (``In [6]``) or pass them later (``In [7]``). Also, IP addresses
can be passed in two ways as a string or tuple (or list). To get list of
headers just call ``get_fields_key()`` method. But this method is a generator,
so in this case we need to cast it. Names convention is pretty simple.
Those names are taken from the RFCs documents.

.. note::

    Some fields are started with the underscrored prefix. This has a special
    meaning. These fields may auto-generate values. So usually, we don't need
    to care about them. But if you want to modify them - feel free to break
    your packets ;)


TCP and Payload protocols
-------------------------

What next? TCP header and some payload for it..

.. code-block:: python

    In [9]: tcp = umit.umpa.protocols.TCP()

    In [10]: tcp.source_port = 2958

    In [11]: tcp.destination_port = 0

    In [12]: tcp.set_flags('control_bits', syn=True)

    In [13]: payload = umit.umpa.protocols.Payload()

    In [14]: payload.data = "this is umpa!"

    In [15]: 

Completely simple so far, isn't it?


protocols container
-------------------

Ok, let's build a packet...

.. code-block:: python

    In [15]: first_packet = umit.umpa.Packet(ip, tcp)

    In [16]: first_packet.include(payload)

So, we passed 2 protocols into constructor, and included another one with the
`include()` method.

Please remember that including order is important. By default, we can't break
the OSI model, so protocols need to be packed in the proper order. Otherwise,
the ``UMPAStrictException`` will raise. If you want to break this rule, please
read about ``strict`` attribute of the Packet's object in later tutorials.

print statement
---------------

If we take a coffe break (longer than 5 hours) now, perhaps we will forget what
we built. Just print it!

.. code-block:: python


    In [17]: print first_packet
    Packet contains 3 protocols
    +-< IP                          >
    | \
    | +-[ Version                   ]		4 (auto - 4)
    | +-[ IHL                       ]		None (auto - 5)
    | +-[ TOS                       ]
    | | \
    | |  -{ precedence0             }		0
    | |  -{ precedence1             }		0
    | |  -{ precedence2             }		0
    | |  -{ delay                   }		0
    | |  -{ throughput              }		0
    | |  -{ relibility              }		0
    | |  -{ reserved0               }		0
    | |  -{ reserved1               }		0
    | | /
    | \-[ TOS                       ]		contains 8 bit flags
    | +-[ Total Length              ]		None (auto - 0)
    | +-[ Identification            ]		0 (auto - 0)
    | +-[ Flags                     ]
    | | \
    | |  -{ reserved                }		0
    | |  -{ df                      }		0
    | |  -{ mf                      }		0
    | | /
    | \-[ Flags                     ]		contains 3 bit flags
    | +-[ Fragment Offset           ]		0 (auto - 0)
    | +-[ TTL                       ]		64 (auto - 64)
    | +-[ Protocol                  ]		None (auto - 0)
    | +-[ _Header Checksum          ]		0 (auto - 0)
    | +-[ Source Address            ]		127.0.0.1
    | +-[ Destination Address       ]		(67, 205, 14, 183)
    | +-[ Options                   ]
    | | \
    | | /
    | \-[ Options                   ]		contains 0 bit flags
    | +-[ Padding                   ]		0 (auto - 0)
    \-< IP                          >		contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xb78c2a4c>
    +-< TCP                         >
    | \
    | +-[ Source Port               ]		2958
    | +-[ Destination Port          ]		0
    | +-[ Sequence Number           ]		None (auto - 0)
    | +-[ Acknowledgment Number     ]		None (auto - 1)
    | +-[ DataOffset                ]		None (auto - 5)
    | +-[ Reserved                  ]		0 (auto - 0)
    | +-[ Control Bits              ]
    | | \
    | |  -{ urg                     }		0
    | |  -{ ack                     }		0
    | |  -{ psh                     }		0
    | |  -{ rst                     }		0
    | |  -{ syn                     }		1
    | |  -{ fin                     }		0
    | | /
    | \-[ Control Bits              ]		contains 6 bit flags
    | +-[ Window                    ]		None (auto - 512)
    | +-[ Checksum                  ]		None (auto - 0)
    | +-[ Urgent Pointer            ]		None (auto - 0)
    | +-[ Options                   ]
    | | \
    | | /
    | \-[ Options                   ]		contains 0 bit flags
    | +-[ Padding                   ]		0 (auto - 0)
    \-< TCP                         >		contains 12 fields
    <umit.umpa.protocols.TCP.TCP object at 0xb78e774c>
    +-< Payload                     >
    | \
    | +-[ Data                      ]		this is umpa!
    \-< Payload                     >		contains 1 fields
    <umit.umpa.protocols.Payload.Payload object at 0xb78e794c>
    <umit.umpa._packets.Packet object at 0xb78e798c>

    In [18]: 


sockets
-------

Now, we are ready to send the packet!
To create a new socket, we will use ``umit.umpa.Socket`` class.
Please remember, that we dropped our priviliges so we need to get them
back now.

We can do it in 2 ways.
1. atomic way (*recommended*)

.. code-block:: python

    In [18]: sock = umit.umpa.utils.security.super_priviliges(umit.umpa.Socket)

    In [19]: 

2. normal way

.. code-block:: python

    In [18]: umit.umpa.utils.security.drop_priviliges()

    In [19]: umit.umpa.utils.security.super_priviliges()

    In [20]: sock = umit.umpa.Socket()

    In [21]: umit.umpa.utils.security.drop_priviliges()

    In [22]: 

Both are correct. But the former is recommended. How does it work?

We pass arguments into ``super_priviliges()`` function, the first has to
be callable, others are just arguments for the first one.
Result of the callable argument is returned by the ``super_priviliges()``
function.

Internally in the ``super_priviliges()`` function:
 1. change EUID to the 0 (root)
 2. call the first argument from passed arguments
 3. change EUID to nobody (call ``drop_priviliges()``)
 4. return the result of the calling from point 2

Ok, actually we have a socket object, so let's send the packet!

.. code-block:: python

    In [19]: sock.send(first_packet)
    Out [19]: [53]

    In [20]:

``Socket.send()`` method returns a list with sent bytes of each packets (we can
pass more than one packet at the same time).


UDP protocol
------------

Ok, let's create another packet with a UDP header just in single line!

.. code-block:: python

    In [20]: udp = umit.umpa.protocols.UDP(source_port=0, destination_port=7)

    In [21]:


ttl aka enumfield
-----------------

Now, we can simple create a new packet and use already created ``sock`` object
to send it out, but before we will do that, lets change TTL field of
the IP protocol.

Some common fields like TTL or ports in TCP/UDP headers are ``EnumField``
objects. What does it mean? Well, this is a simple numeric field but with
special behaviour.
We can pass common names instead of numbers (what is easier to remember).
Let's do it on the TTL example.

.. code-block:: python

    In [21]: ip.get_field("time_to_live").enumerable
    Out[21]: 
    {'aix': 60,
     'dec': 30,
     'freebsd': 64,
     'irix': 60,
     'linux': 64,
     'macos': 60,
     'os2': 64,
     'solaris': 255,
     'sunos': 60,
     'ultrix': 60,
     'windows': 128}

    In [22]: ip.time_to_live = "windows"

    In [23]: 

Why can't we use ``ip.time_to_live.enumerable`` in the first line?
Well, attributes like object.''name_of_field'' are reserved only to get/set
values of them. They handle only with values. To get a reference to the field's
object we need to use ``get_field()`` method.

print statement is sooo cool
----------------------------

Don't forget about checking if everything is correct :-)

.. code-block:: python

    In [23]: print second_packet
    Packet contains 2 protocols
    +-< IP                          >
    | \
    | +-[ Version                   ]		4 (auto - 4)
    | +-[ IHL                       ]		None (auto - 5)
    | +-[ TOS                       ]
    | | \
    | |  -{ precedence0             }		0
    | |  -{ precedence1             }		0
    | |  -{ precedence2             }		0
    | |  -{ delay                   }		0
    | |  -{ throughput              }		0
    | |  -{ relibility              }		0
    | |  -{ reserved0               }		0
    | |  -{ reserved1               }		0
    | | /
    | \-[ TOS                       ]		contains 8 bit flags
    | +-[ Total Length              ]		None (auto - 28)
    | +-[ Identification            ]		0 (auto - 0)
    | +-[ Flags                     ]
    | | \
    | |  -{ reserved                }		0
    | |  -{ df                      }		0
    | |  -{ mf                      }		0
    | | /
    | \-[ Flags                     ]		contains 3 bit flags
    | +-[ Fragment Offset           ]		0 (auto - 0)
    | +-[ TTL                       ]		128 (auto - 128)
    | +-[ Protocol                  ]		None (auto - 17)
    | +-[ _Header Checksum          ]		0 (auto - 0)
    | +-[ Source Address            ]		127.0.0.1
    | +-[ Destination Address       ]		(67, 205, 14, 183)
    | +-[ Options                   ]
    | | \
    | | /
    | \-[ Options                   ]		contains 0 bit flags
    | +-[ Padding                   ]		0 (auto - 0)
    \-< IP                          >		contains 14 fields
    <umit.umpa.protocols.IP.IP object at 0xb78c8b6c>
    +-< UDP                         >
    | \
    | +-[ Source Port               ]		0
    | +-[ Destination Port          ]		7
    | +-[ Length                    ]		None (auto - 8)
    | +-[ Checksum                  ]		None (auto - 0)
    \-< UDP                         >		contains 4 fields
    <umit.umpa.protocols.UDP.UDP object at 0xb78c8b0c>
    <umit.umpa._packets.Packet object at 0xb78c8ecc>

    In [24]: 

As you see, TTL is "in Windows mode".

packing and sending again
-------------------------

.. code-block:: python

    In [24]: second_packet = umit.umpa.Packet(ip, udp)

    In [25]: sock.send(first_packet, second_packet)
    Out [25]: [53, 28]

    In [26]:

We sent 2 packets. 53 bytes first for the first packet and 28 for the second.

Now, just make some exercises to get more practice!
