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
Internal Exceptions for the library.
"""

class UMPAException(Exception):
    """
    General Exception.
    """

    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class UMPAAttributeException(UMPAException):
    """
    Exception related to attributes issues.

    It's being used if someone try to acces to undefined field etc.
    """

    pass

class UMPAStrictException(UMPAException):
    """
    Exception related to strict packets issue.

    If strict attribute of the Packet's object is True and
    the order of protocols is odd then the exception is raised.
    """

    pass

class UMPANotPermittedException(UMPAException):
    """
    Exception related to system permissions issues."
    """

    def __str__(self):
        return repr(self.msg) + ("\n\tIt's recommended to use "
                        "umpa.utils.security module to avoid the exception.")
