================
 Plugins System
================

Introduction
============

How plugins system works in UMPA and how to write your own extension
or protocol.


Overview
========

UMPA has not a real plugin system. But there is an imitation of this and it
works very well.

There are 2 independent groups of plugins:
 1. protocols
 2. extensions

Each of them work in different way, a structure of plugins are completely
different. The only similar thing is a location for local plugins.

So, there are provided some plugins with UMPA. Extensions like XML or schedule.
Protocols like IP or TCP. As you have already known, we can use them in very
simple way just by importing them.

.. code-block:: python

    import umit.umpa.extensions.XML
    from umit.umpa.extensions import schedule

    import umit.umpa.protocols.IP

But we can write our owns plugins and store them in our $HOME directory.
By importing UMPA first time, it will create a special directory $HOME/.umpa
and this directory is important keep some configs and plugins. There is
a sub-directory ``$HOME/.umpa/umpa_plugins`` with ``extensions`` and
``protocols`` sub-directories. So you can keep your own plugins there.

Because it's just an imitation of the real plugins system, there is no
interface, and no real API for it. In fact, we can just write normal modules,
like the core code of the UMPA. So, sometimes we need to handle with private
"things". I know, it's ugly. I'm going to rewrite it someday. Sorry about this!


available plugins
-----------------

There are 3 functions for ``umit.umpa.protocols`` and ``umit.umpa.extensions``
to get available protocols/extensions:

 * ``get_all()`` - return both local and global plugins
 * ``get_globals()`` - return only global plugins
 * ``get_locals()`` - return only local plugins

.. note::
    protocols' plugins are loaded automatically, but extensions' plugins not.


Protocols
=========

Firstly, just read any already implemented protocols to see how it works.

But here is pointed some important issues.

There are 3 common modules which we should use to create new protocol
implementation:

 1. ``umit.umpa.protocols._protocols`` -- with our the super-class ``Protocol``
 2. ``umit.umpa.protocols._fields`` -- with many common classes of fields
 3. ``umit.umpa.protocols._consts`` -- with common constansts

protocol class in general
-------------------------

Ok, let's call our protocol ``Foo`` and create class.

.. code-block:: python

    from umit.umpa.protocols import _protocols
    from umit.umpa.protocols import _fields

    class Foo(Protocol):
        layer = 4                                                             # layer of OSI model where protocol is situated
        protocol_id = 1234                                                    # read below >> 1 <<
        name = "Foo"                                                          # name of the protocol, usually the same as name of the class

        _ordered_fields = ('field1', 'field2', '_field3')                     # read below >> 2 <<

        def __init__(self, **kwargs):
            flags = ('bit1', 'bit2')                                          # read below >> 3 <<
            flags_predefined = dict.fromkeys(flags, 0)

            fields_list = [ _HField1("Field1"),                               # read below >> 4 <<
                            _fields.Flags("Flags", flags, **flags_predefined),
                            _HField3("Field3", 666)
                          ]

            super(Foo, self).__init__(fields_list, **kwargs)                  # read below >> 5 <<

            
OK, we've already created our ``Foo`` class. It's not finished yet but...:)
The most obvious lines are commented in the line-comment. The rest is below:

 1. ``protocol_id`` class attribute is an general attribite for any ID of
    the protocol. Usually it's used by a lower layer for information what
    protocol is upper. E.g. in Ethernet protocol there is a field EtherType
    and there will be 0x0800 if upper protocol is IP.
    So, in this case protocol_id for IP should be 0x0800.

 2. ``_ordered_fields`` -- this is a tuple of fields in the order as we want
    to see it in the header of our protocol. Items of the tuple are names of
    fields. User uses these names like ``foo.field1`` if he wants to access
    to them. Please note about underscored '_' prefix. It says that the field
    is auto-filling and shouldn't be modify by the user.

 3. The second field is a flag-type. Like control bits field in TCP with
    bit flags like SYN, FIN, ACK etc. Items the tuple are names of each
    bit-flag. The next line predefined them to default values (0 for every bits
    in this case).

 4. This list contains fields-objects. We can use already written classes
    provided by ``umit.umpa.protocols._fields`` (like ``Flags``) or create new
    subclasses as we are going to do with two fields. Arguments for constructor
    are: ``name, value=None, bits=None, auto=None``. We define a default value
    form Field3 but omit rest because we will set them in classes directly.
    Please note, that the order of the list must be same as the order
    of ``_ordered_fields`` tuple.

 5. We call a constructor from ``Protocol``. It handles with \*\*kwargs and
    set a lot of things for us.

We need to implement 2 methods, but let's take care about our 2 fields first.


fields classes
--------------

``_H`` prefix for classes names is only a pattern. I like it, you don't have to.
Every field's class has to inherit from the ``umit.umpa.protocols.fields.Field``
class or subclasses. Our fields are number-type. Field1 should be set by user,
and Field3 is auto-filling.

.. code-block:: python

    import random

    class _HField1(_fields.IntField):
        bits = 8
        auto = False
        
    class _HField3(_fields.IntField):
        bits = 4
        auto = True

        def _generate_value(self):
             return random.randint(0, 15)

As you see the first field is pretty simple. We set a length of it in bits,
and auto attribute. Because it has to be set manually, we don't have to do
anything more. If user doesn't set the value, the ``UMPAException`` will raise.
It will happen because:

 1) we don't have any value (default or set by user),
 2) we don't have overridden ``_generate_value()`` method.

Pretty simple isn't?

For the Field3 we implemented ``_generate_value()`` method and it returns
random numbers. But, please remember that we set default value of the field
to 666. So, it won't call ``_generate_value()`` unless user clear the current
value of the field.


pre/post raw methods
--------------------

Ok, we left two methods from our ``Foo`` class, so let's implement them now.
They are called ``_pre_raw()`` and ``_post_raw()``.

Usually we can just return 2 arguments and skip them but for some cases we need
to write a bit more. Some fields depend on other fields or on protocols from
other layers. For example checksum header fields handles with other fields.
This issue is a bit advanced, so if you are interest how to solve it, read
the code of IP and TCP implementations and about ``SpecialIntField`` class.
These protocols have several fields which handle with others and they cover
most of the cases. If you need a help, please contact with us. Perhaps, we will
write an example of this as well.

For our example - this code is enough:

.. code-block:: python

    def _pre_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit

    def _post_raw(self, raw_value, bit, protocol_container, protocol_bits):
        return raw_value, bit


last lines of the code
----------------------

Ok, we have already implemented successfully our Foo protocol. We only need to
add 2 lines at the end of the file:

.. code-block:: python

    protocols = [ Foo, ]
    __all__ = [ "Foo", ]

The ``protocols`` list is used by the plugin mechanism. If we store our module
in ``$HOME/.umpa/umpa_plugins/protocols``, it will be automatically loaded by
``import umit.umpa.protocols``. We can just import the class
by ``from umit.umpa.protocols import Foo``. Also, we can check our protocols'
plugins by calling ``umit.umpa.protocols.get_locals()``.


Extensions
==========

This kind of plugins is fairly simple. And in fact, there is no any API.


new extension: the hacker
-------------------------

Let's create an extenstion which will print into STDERR "Hello <name>, you are
the real hacker!" phrase.

All we really need is:

.. code-block:: python

    import sys

    def say_hello(name):
       print >> sys.stderr, "Hello %s, you are the real hacker!" % name

Yep, that it!

loading extensions
------------------

If we store the extension in ``$HOME/.umpa/umpa_plugins/extensions/hacker.py``,
we have 2 ways to import it.

.. code-block:: python

    # first way
    import umpa_plugins.extensions.hacker

    # second way
    import umit.umpa.extensions
    umit.umpa.extensions.load_extension('hacker')

After that, we can simple call the new extension if we want it.

.. code-block:: python

umpa_plugins.extensions.hacker.say_hello("Alice")    # for the former importing style

umit.umpa.extensions.hacker.say_hello("Bob")         # for the second one


extending the hacker
--------------------

Because UMPA is written in the Python we can dynamically add something to our
objects. So let's our ``say_hello()`` function as a ``Packet`` method!

.. code-block:: python

    import umit.umpa

    def _say_hello_method(self, name):
        say_hello(name)

    umit.umpa.Packet.say_hello = _say_hello_method

Now, we can call our method for Packet's objects!

As you should noticed, you can override some methods by this way!
So your extension can be completely integrated with UMPA!
