# Copyright (C) 2013-2015 A. Eijkhoudt and others

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

#!/usr/bin/env python
# coding: utf-8

# Base Python modules
import os
import sys
import hashlib
import traceback
import datetime


class File(object):

    def __init__(self, fullpath, config, magic):
        """
        Attempt to parse the file passed via the fullpath variable
        and store its name, size, owner, group, MACtimes,
        MD5/SHA1/SHA256 hashes and file magic  properties in the
        object's properties.
        """
        if not fullpath:
            pass
        else:
            try:
                self.fullpath = str(fullpath)
                self.name = str(os.path.basename(fullpath))
                self.size = str(os.path.getsize(fullpath))
            except:
                raise IOError("""Cannot read basic file information.
                                Permissions problem?""")
            try:
                self.owner = str(os.stat(fullpath).st_uid)
                self.group = str(os.stat(fullpath).st_gid)
            except:
                self.owner = -1
                self.group = -1
                if config.DEBUG:
                    print("""Cannot read owner/group id.
                            File system might not support ownerships.""")
            try:
                self.perm = oct(os.stat(fullpath).st_mode)
            except:
                self.perm = 'UFORIA_NO_PERM'
                if config.DEBUG:
                    print("""Cannot read permissions.
                            File system might not support permissions.""")
            try:
                timestamp = os.path.getmtime(fullpath)
                self.mtime = datetime.datetime.fromtimestamp(timestamp).isoformat()
            except:
                self.mtime = Null
                if config.DEBUG:
                    print('File system might not support MACtimes.')
            try:
                timestamp = os.path.getatime(fullpath)
                self.atime = datetime.datetime.fromtimestamp(timestamp).isoformat()
            except:
                self.atime = Null
                if config.DEBUG:
                    print('File system might not support MACtimes.')
            try:
                timestamp = os.path.getctime(fullpath)
                self.ctime = datetime.datetime.fromtimestamp(timestamp).isoformat()
            except:
                self.ctime = Null
                if config.DEBUG:
                    print('File system might not support MACtimes.')
            try:
                self.md5 = hashlib.md5()
                self.sha1 = hashlib.sha1()
                self.sha256 = hashlib.sha256()
                with open(fullpath, 'rb') as f:
                    for chunk in iter(lambda: f.read(config.CHUNKSIZE), b''):
                        self.md5.update(chunk)
                        self.sha1.update(chunk)
                        self.sha256.update(chunk)
                self.md5 = str(self.md5.hexdigest())
                self.sha1 = str(self.sha1.hexdigest())
                self.sha256 = str(self.sha256.hexdigest())
            except:
                traceback.print_exc(file=sys.stderr)
            try:
                magic_default = magic.Magic(magic_file=config.MAGICFILE)
                magic_mime = magic.Magic(mime=True,
                                         magic_file=config.MAGICFILE)
            except:
                traceback.print_exc(file=sys.stderr)
            try:            
                self.ftype = str(magic_default.from_file(fullpath))
                self.mtype = str(magic_mime.from_file(fullpath))
                self.btype = str(magic_default.from_buffer(open(fullpath).read(65536)))
            except:
                traceback.print_exc(file=sys.stderr)
            if config.DEBUG:
                print "Filename:\t", self.name
                print "UID/GID:\t", self.owner + ":" + self.group
                print "Permissions:\t", self.perm
                print ("Magic:\t\tF:", self.ftype, "\n\t\tM:",
                       self.mtype, "\n\t\tB:", self.btype)
                print ("Modified:\t", self.mtime, "\nAccessed:\t",
                       self.atime, "\nChanged:\t", self.ctime)
                print ("MD5:\t\t", self.md5, "\nSHA1:\t\t",
                       self.sha1, "\nSHA256:\t\t", self.sha256)
