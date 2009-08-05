============
 Extensions
============

Introduction
============

You will read short overview about extensions and learn how to use already
provided ones.


Overview
========

Extensions add extra features and/or functionality for UMPA. They are not
necessary to correct usage of the library, but they may make your life easier.

Extensions are module-oriented. Usually they provide independent functions and
add similar methods for objects. Also they can change behaviour of the objects.
But they are not imported automatically, so if you don't import them, there is
no risk of odd objects behaviour at all.

There is a one function provided by ``umit.umpa.extensions`` package.
It's called ``load_extensions()``. But it's not necessary to use it here. Read
more about this function in next tutorial.


XML
===

XML is a markup language for documents containing structured information.
We can save and restore packets/protocols with XML.

XML extension uses DOM. Files are relatively small, so there is no need
to use SAX. But, perhaps it will be rewritten with SAX someday..

save packets to the file
------------------------

Let's create a packet (the same one TCP/IP packet as we created in our first
tutorial).

.. code-block:: python

    import umit.umpa
    import umit.umpa.utils.security

    from umit.umpa.protocols import IP, TCP, Payload

    # droping priviliges
    umit.umpa.utils.security.drop_priviliges()

    # IP header
    ip = IP()
    ip.source_address = "127.0.0.1"
    ip.destination_address = "67.205.14.183"

    # TCP header
    tcp = TCP()
    tcp.source_port = 2958
    tcp.destination_port = 0
    tcp.set_flags('control_bits', syn=True)

    # Payload
    data = Payload()
    data.data = "this is umpa!"

    # packet
    packet = umit.umpa.Packet(ip, tcp, data)

So, let's store it as a XML file on the harddrive.

.. code-block:: python

    from umit.umpa.extensions import XML

    XML.save('packet.xml', (packet,))

Second ``save()`` function's argument is a list. We can save more than
one packet in the single file.

So, we have sucessfully stored our packet. Let's read the XML file.

.. code-block:: xml

    <?xml version="1.0" ?>
    <UMPA>
        <packet id="0" strict="True">
            <protocol class="umit.umpa.protocols.IP.IP">
                <_version type="int">
                    4
                </_version>
                <_ihl type="NoneType">
                    None
                </_ihl>
                <type_of_service type="bits">
                    <relibility type="bool">
                        False
                    </relibility>
                    <reserved0 type="bool">
                        False
                    </reserved0>
                    <delay type="bool">
                        False
                    </delay>
                    <throughput type="bool">
                        False
                    </throughput>
                    <reserved1 type="bool">
                        False
                    </reserved1>
                    <precedence2 type="bool">
                        False
                    </precedence2>
                    <precedence1 type="bool">
                        False
                    </precedence1>
                    <precedence0 type="bool">
                        False
                    </precedence0>
                </type_of_service>
                <_total_length type="NoneType">
                    None
                </_total_length>
                <_identification type="int">
                    0
                </_identification>
                <flags type="bits">
                    <df type="bool">
                        False
                    </df>
                    <mf type="bool">
                        False
                    </mf>
                    <reserved type="bool">
                        False
                    </reserved>
                </flags>
                <_fragment_offset type="int">
                    0
                </_fragment_offset>
                <time_to_live type="int">
                    64
                </time_to_live>
                <_protocol type="NoneType">
                    None
                </_protocol>
                <_header_checksum type="int">
                    0
                </_header_checksum>
                <source_address type="str">
                    127.0.0.1
                </source_address>
                <destination_address type="str">
                    67.205.14.183
                </destination_address>
                <options type="bits"/>
                <_padding type="int">
                    0
                </_padding>
            </protocol>
            <protocol class="umit.umpa.protocols.TCP.TCP">
                <source_port type="int">
                    2958
                </source_port>
                <destination_port type="int">
                    0
                </destination_port>
                <_sequence_number type="NoneType">
                    None
                </_sequence_number>
                <_acknowledgment_number type="NoneType">
                    None
                </_acknowledgment_number>
                <_data_offset type="NoneType">
                    None
                </_data_offset>
                <_reserved type="int">
                    0
                </_reserved>
                <control_bits type="bits">
                    <psh type="bool">
                        False
                    </psh>
                    <urg type="bool">
                        False
                    </urg>
                    <ack type="bool">
                        False
                    </ack>
                    <syn type="bool">
                        True
                    </syn>
                    <rst type="bool">
                        False
                    </rst>
                    <fin type="bool">
                        False
                    </fin>
                </control_bits>
                <_window type="NoneType">
                    None
                </_window>
                <_checksum type="NoneType">
                    None
                </_checksum>
                <_urgent_pointer type="NoneType">
                    None
                </_urgent_pointer>
                <options type="bits"/>
                <_padding type="int">
                    0
                </_padding>
            </protocol>
            <protocol class="umit.umpa.protocols.Payload.Payload">
                <data type="str">
                    this is umpa!
                </data>
            </protocol>
        </packet>
    </UMPA>

Isn't it look so nice? :)


restore the packet
------------------

Just call ``load()`` function!

.. code-block:: python

    packets = XML.load('packet.xml')

``packets`` is a list of loaded packets. If we need the first packet from the
list, just do something like

.. code-block:: python

    packet = XML.load('packet.xml')[0]

What if we have a packet's object and we just want to load protocols from the
file into the object?

.. code-block:: python

    packet.protos = XML.load('packet.xml', proto_only=True)

With ``proto_only=True load()`` function loads *ONLY* first packet and
returns *ONLY* protocols (instead of the packet's object).

Huh, this case doesn't look so nice, does it? Let's do the same
in object-oriented style!


object-oriented XML
-------------------

Let's back to the state when we created our packet...

.. code-block:: python

    import umit.umpa.extensions.XML

    packet.save_xml('packet.xml')

    another_packet = umit.umpa.Packet()
    another_packet.load_xml('packet.xml')

By importing XML extensions Packet objects get 2 extra methods (``save_xml()``
and ``load_xml()``). It's so simple now!

.. warning:: 
    ``another_packet`` *is not* exactly the same as ``packet``!
    ``id()`` results vary. They have the same values but this is different
    instance of the Packet class.

 

schedule
========

This extension adds extra features for ``Socket`` objects. It helps us to keep
control when to send our packets.


delay
-----

If we call ``Socket.send()`` method, passed packets will be sent immediately.
We can make a delay for this in 2 ways: by calling function (``send()``) from
the extension or calling new method of Socket's object. In general, both ways
are the same, they have a minor difference, we will talk about it later 

.. code-block:: python

    import umit.umpa
    import umit.umpa.extensions.schedule

    sock = umit.umpa.Socket()
    sock.send_schedule(5, packet1, packet2)

UMPA will wait 5 seconds before send 2 packets.


extra options
-------------

There are 3 extra options which can be passed. Let's describe them!

interval
````````

If we want to send more than one packet at once, we may add interval
between them. It means, UMPA will sleep between sending next packets.

.. code-block:: python

    sock.send_schedule(5, packet1, packet2, interval=2)

In this case, UMPA'll sleep 5 secs at the beginning, and additional 2 secs
after ``packet1`` will be sent.


socket
``````

Here is that minor difference between ``umit.umpa.extensions.schedule.send()``
function and ``send_schedule()`` method.

We don't use this option for the method. It's set to the ``self`` by default.

So, let's focus on the function. If we don't pass the socket option,
the extension will create new ``umit.umpa.Socket`` object for us,
and will use it.

But we can pass the already created object instead.

.. code-block:: python

    import umit.umpa
    import umit.umpa.extensions.schedule

    sock = umit.umpa.Socket()

    umit.umpa.extensions.schedule.send(0, packet1, packet2, interval=10, socket=sock)

In this case we're sending 2 packets with 10 secs delay between them,
but without a delay at the beginning. Also the extension will not create
a new instance of ``umit.umpa.Socket``, just use passed ``sock`` object
instead.

detach
``````

When we set a delay or interval, our process/application is being blocked till
everything will be sent out. By using detach option, sending is done
in backgroung and we can go with next instructions.

.. code-block:: python

    import umit.umpa
    import umit.umpa.extensions.schedule

    umit.umpa.extensions.schedule.send(10, packet1, packet2, interval=5, detach=True)
    print "we can print something immediately"

In this case, the print statement is run without waiting till both packets will
be sent out (they will be in a background after set delays).
