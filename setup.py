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
import os
import os.path
from stat import ST_MODE
from distutils.core import setup
from distutils.command.install import install

UMPA_VERSION = '0.2'

TESTS_DIR = [
    os.path.join('tests'),
    os.path.join('tests', 'system'),
    os.path.join('tests', 'system', 'test_snd'),
    os.path.join('tests', 'system', 'test_sndrcv'),
    os.path.join('tests', 'a_unit'),
    os.path.join('tests', 'a_unit', 'test_extensions'),
    os.path.join('tests', 'a_unit', 'test_protocols'),
    os.path.join('tests', 'a_unit', 'test_utils'),
    os.path.join('tests', 'a_unit', 'test_sniffing'),
    os.path.join('tests', 'a_unit', 'test_sniffing', 'test_libpcap'),
]

class umpa_install(install):
    def run(self):
        install.run(self)
        self.create_uninstaller()

    def create_uninstaller(self):
        uninstaller_filename = os.path.join(
                self.install_data, 'share', 'umpa', 'uninstall_umpa')
        uninstaller = []
        uninstaller.append(
                "#!/usr/bin/env python\n"
                "import os, sys, shutil\n"
                "\n"
                "print\n"
                "print '%(line)s Uninstall UMPA %(version)s %(line)s'\n"
                "print\n"
                "\n"
                "answer = raw_input('Are you sure that you want to '\n"
                "        'completly uninstall UMPA %(version)s? (yes/no) ')\n"
                "\n"
                "if answer.lower() not in ['yes', 'y']:\n"
                "    sys.exit(0)\n"
                "\n"
                "print\n"
                "print '%(line)s Uninstalling UMPA %(version)s... %(line)s'\n"
                "print\n" % {'version': UMPA_VERSION, 'line': '-' * 10})

        for output in self.get_outputs():
            uninstaller.append(
                    'print "Removing %(output)s..."\n'
                    'if os.path.exists("%(output)s"):\n'
                    '    os.remove("%(output)s")\n' % {'output': output})

        uninstaller.append(
                "print 'Removing uninstaller itself...'\n"
                "os.remove('%s')\n" % uninstaller_filename)

        uninstaller.append('print "Removing empty directories..."\n')
        for dir in (
                os.path.join(self.install_data, 'share', 'umpa'),
                os.path.join(self.install_data, 'share', 'doc', 'umpa'),
                os.path.join(self.install_lib, 'umpa'),
            ):
            uninstaller.append(
                    'if os.path.exists("%(dir)s"):\n'
                    '    shutil.rmtree("%(dir)s")\n' % {'dir' : dir})

        uninstaller_file = open(uninstaller_filename, 'w')
        uninstaller_file.writelines(uninstaller)
        uninstaller_file.close()

        # Set exec bit for uninstaller
        mode = ((os.stat(uninstaller_filename)[ST_MODE]) | 0555) & 07777
        os.chmod(uninstaller_filename, mode)

cmdclasses = {
        'install' : umpa_install,
        }

test_files = []
for dir in TESTS_DIR:
    test_files = test_files + [ (os.path.join('share','umpa', dir),
                                glob.glob(os.path.join(dir,'*.py')))]

data_files = [  (os.path.join('share','umpa','examples'),
                            glob.glob(os.path.join('examples','*'))),
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
        data_files = data_files,
        cmdclass = cmdclasses,
)
