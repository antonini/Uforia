# Copyright (C) 2013 Hogeschool van Amsterdam

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Stores the CAB file metadata and starts Uforia recursively on the
# files inside the CAB folder.

# TABLE: Signature:LONGTEXT, Offset:INT, cabversion:LONGTEXT, Folder:INT, Files:INT, OffsetFirstFile:INT, Compression:INT, Checksum:INT, SizeCompBytes:INT, SizeUnCompBytes:INT, PositionFirst:INT, WinCEHeader:INT, TargetArch:INT, MinWinCEVersion:INT, MaxWinCeVersion:INT, MinBuildNo:INT

import sys
import traceback
import tempfile
import imp
import shutil
import os
import subprocess
import recursive
from struct import *


def process(fullpath, config, rcontext, columns=None):
    try:
        # Get instance of 7z module
        zip_module = imp.load_source('7zfilerecursor',
                                     'modules/application/' +
                                     'x-7z-compressed/7zfilerecursor.py')
        
        # Open cab file for reading
        file = open(fullpath, 'rb')
        assorted = [file.read(4)]
        cabhdr = unpack('iiiiibbhhhhh', file.read(32))

        assorted.append(cabhdr[3])
        version = "%d.%d" % (cabhdr[6], cabhdr[5])
        assorted.append(version)
        assorted.append(cabhdr[7])
        assorted.append(cabhdr[8])

        if cabhdr[9] > 3:
            print "CAB9 > 3"
            resv = unpack('hbb', file.read(4))

        cabflr = unpack('ihh', file.read(8))
        assorted.append(cabflr[0])
        assorted.append(cabflr[2])
        if cabflr[2] >= 0:
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
            assorted.append(None)
        else:
            file.seek(cabflr[0])
            cfdata = unpack('ibh', file.read(8))
            assorted.append(cfdata[0])
            assorted.append(cfdata[1])
            assorted.append(cfdata[2])
            assorted.append(file.tell())

            assorted.append(file.read(4))

            cehdr = unpack('iiiiiiiiiii', file.read(44))

            assorted.append(cehdr[4])
            minimum_ce_version = "%d.%d" % (cehdr[5], cehdr[6])
            maximum_ce_version = "%d.%d" % (cehdr[7], cehdr[8])
            minimum_build_number = "%d.%d" % (cehdr[9], cehdr[10])
            assorted.append(minimum_ce_version)
            assorted.append(maximum_ce_version)
            assorted.append(minimum_build_number)

        # Try to extract the content of the 7zip file.
        try:
            # Get instance of 7z module
            zip_module = imp.load_source('7zfilerecursor',
                                     'modules/application/' +
                                     'x-7z-compressed/7zfilerecursor.py')

            # Create a temporary directory
            tmpdir = tempfile.mkdtemp("_uforiatmp", dir=config.EXTRACTDIR)

            # Extract the 7zip file
            zip_module._extractall(fullpath, tmpdir, config.SEVENZIP_TOOL)

            recursive.call_uforia_recursive(config, rcontext, tmpdir, fullpath)
        except:
            traceback.print_exc(file=sys.stderr)

        # Delete the temporary directory, proceed even if it causes
        # an error
        try:
            pass
            shutil.rmtree(tmpdir)
        except:
            traceback.print_exc(file=sys.stderr)

        assert len(assorted) == len(columns)

        # Print some data that is stored in the database if debug is true
        if config.DEBUG:
            print "\nCab file data:"
            for i in range(0, len(assorted)):
                print "%-18s %s" % (columns[i] + ':', assorted[i])

        return assorted

    except:
        traceback.print_exc(file=sys.stderr)

        # Store values in database so not the whole application crashes
        return None
