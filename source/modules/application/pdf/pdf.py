# Copyright (C) 2013 Hogeschool van Amsterdam

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


#!/usr/bin/env python

# TABLE: creation_date:TEXT, modified_date:TEXT, save_date:TEXT, author:TEXT, producer:TEXT, page_count:INT, content:LONGTEXT


import string
import tika
import recursive
import traceback
import tempfile
import shutil
import os
import sys
import subprocess


def _extractall(fullpath, tempdir):
    # Path that leads to the archive
    if fullpath is None:
        raise Exception("Archive path not given")

    # Path that leads to the destination
    if tempdir is None:
        raise Exception("Tempdir not given")

    # Set tika location
    tika_jar_path = os.path.abspath("./libraries/tika/tika-app-1.3.jar")
    if not os.path.exists(tika_jar_path):
        raise Exception("Tika not found at " + tika_jar_path)
    
    p = subprocess.Popen(["java",
                          "-jar",
                          tika_jar_path,
                          "--extract",
                          fullpath],
                         cwd=tempdir)
    output = p.communicate()[0]

    if output is not None:
        raise Exception("tika extract command failed") 

def process(fullpath, config, rcontext, columns=None):
    parser = tika.AutoDetectParser()

    input = tika.FileInputStream(tika.File(fullpath))

    content = tika.BodyContentHandler()
    metadata = tika.Metadata()
    context = tika.ParseContext()
    
    parser.parse(input,content,metadata,context)
    content = content.toString()

    processed = [
        metadata.get("Creation-Date"),
        metadata.get("Last-Modified"),
        metadata.get("Last-Save-Date"),
        metadata.get("Author"),
        metadata.get("producer"),
        metadata.get("xmpTPg:NPages"),
        content
    ]

    # To skip recursive call if there are no files to extract
    extractor = tika.ParserContainerExtractor()
    needs_extraction = extractor.isSupported(tika.TikaInputStream.get(input))

    if needs_extraction:
        # Call Uforia recursively on embedded files
        tempdir = None
        try:
            # Perform extraction
            tmpdir = tempfile.mkdtemp(dir=config.EXTRACTDIR)
            _extractall(fullpath, tmpdir)

            # Call Uforia again
            recursive.call_uforia_recursive(config, rcontext, tmpdir, fullpath) 
        except:
            traceback.print_exc(file=sys.stderr)
        finally:    
            try:
                if tempdir:
                    shutil.rmtree(tmpdir)  # delete directory
            except OSError as exc:
                traceback.print_exc(file=sys.stderr)

    return processed
