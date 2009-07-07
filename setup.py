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

import glob
import os.path
from distutils.core import setup

UMPA_VERSION = '0.2'


TESTS_DIR = [
    os.path.join('tests'),
    os.path.join('tests', 'system'),
    os.path.join('tests', 'system', 'test_sndrcv'),
    os.path.join('tests', 'a_unit'),
    os.path.join('tests', 'a_unit', 'test_extensions'),
    os.path.join('tests', 'a_unit', 'test_protocols'),
    os.path.join('tests', 'a_unit', 'test_utils'),
    os.path.join('tests', 'a_unit', 'test_sniffing'),
    os.path.join('tests', 'a_unit', 'test_sniffing', 'test_libpcap'),
]

test_files = []
for dir in TESTS_DIR:
    test_files = test_files + [ (os.path.join('share','umpa', dir),
                                glob.glob(os.path.join(dir,'*.py')))]

data_files = [  (os.path.join('share','umpa','examples'),
                            glob.glob(os.path.join('examples','*'))),
                (os.path.join('share','umpa','scripts'),
                    glob.glob(os.path.join('install_scripts','*.sh'))),
                (os.path.join('share','doc','umpa','API'),
                    glob.glob(os.path.join('docs','API','*'))),
                (os.path.join('share','umpa',),
                    ('run_tests.sh', 'run_tests.bat')),
                (os.path.join('share','doc','umpa'),
                    ('README', 'COPYING', 'AUTHORS', 'TODO', 'CHANGES',
                    'INSTALL')),
                (os.path.join('share','umpa','tests'),
                (os.path.join('tests','README'), os.path.join('tests','IMPORTANT'))),
            ] + test_files

setup(  name            = "UMPA",
        version         = UMPA_VERSION,
        description     = "Umit's Manipulations of Packets Art",
        author          = "Bartosz SKOWRON",
        author_email    = "getxsick@gmail.com",
        url             = "http://www.umpa.umitproject.org",
        license         = "GNU LGPLv2",
        platforms       = ["Platform Independent"],
        packages        = [ "umpa",
                            "umpa.protocols",
                            "umpa.sniffing",
                            "umpa.sniffing.libpcap",
                            "umpa.extensions",
                            "umpa.utils",
                            ],
        data_files = data_files

)
