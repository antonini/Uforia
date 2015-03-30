#!/usr/bin/env python

# Copyright (C) 2013-2015 A. Eijkhoudt and others

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# Generic video module using avbin (which is a stable API for libav, a
# fork of the widely used ffmpeg library)

# TABLE: n_streams:INT, start_time:BIGINT, duration:BIGINT, title:LONGTEXT, author:LONGTEXT, copyright:LONGTEXT, comment:LONGTEXT, album:LONGTEXT, year:INT, track:INT, genre:LONGTEXT, width:INT UNSIGNED, height:INT UNSIGNED, sample_aspect:DOUBLE, frame_rate:DOUBLE, sample_format:INT UNSIGNED, sample_rate:INT UNSIGNED, sample_bits:INT UNSIGNED, channels:INT UNSIGNED, allStreams:LONGTEXT


import sys
import traceback
import platform
import ctypes
import libutil


# Definitions of the C structures and functions from AVbin using ctypes
# see: https://github.com/ardekantur/pyglet/blob/master/pyglet/media/avbin.py


class AVbinFileInfo(ctypes.Structure):
    _fields_ = [
        ('structure_size', ctypes.c_size_t),
        ('n_streams', ctypes.c_int),
        ('start_time', ctypes.c_int64),
        ('duration', ctypes.c_int64),
        ('title', ctypes.c_char * 512),
        ('author', ctypes.c_char * 512),
        ('copyright', ctypes.c_char * 512),
        ('comment', ctypes.c_char * 512),
        ('album', ctypes.c_char * 512),
        ('year', ctypes.c_int),
        ('track', ctypes.c_int),
        ('genre', ctypes.c_char * 32), ]


class _AVbinstreamVideo8(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_uint),
        ('height', ctypes.c_uint),
        ('sample_aspect_num', ctypes.c_uint),
        ('sample_aspect_den', ctypes.c_uint),
        ('frame_rate_num', ctypes.c_uint),
        ('frame_rate_den', ctypes.c_uint), ]

# The _num/_den fields will be compressed into one, so we need to track
# the number of fields manually.
AVBIN_STREAM_ACTUAL_NUMBER_OF_VIDEO_INFO_FIELDS = 4


class _AVbinstreamAudio8(ctypes.Structure):
    _fields_ = [
        ('sample_format', ctypes.c_int),
        ('sample_rate', ctypes.c_uint),
        ('sample_bits', ctypes.c_uint),
        ('channels', ctypes.c_uint), ]


class _AVbinstreamUnion8(ctypes.Union):
    _fields_ = [
        ('video', _AVbinstreamVideo8),
        ('audio', _AVbinstreamAudio8), ]


class AVbinstream8(ctypes.Structure):
    _fields_ = [
        ('structure_size', ctypes.c_size_t),
        ('type', ctypes.c_int),
        ('u', _AVbinstreamUnion8)]

AVBIN_STREAM_TYPE_UNKNOWN = 0
AVBIN_STREAM_TYPE_VIDEO = 1
AVBIN_STREAM_TYPE_AUDIO = 2
AVBIN_STREAM_TYPE_STRING_MAPPING = [
    'unknown',
    'video',
    'audio']
AVbinStreamType = ctypes.c_int

AVBIN_LOG_QUIET = -8
AVBIN_LOG_PANIC = 0
AVBIN_LOG_FATAL = 8
AVBIN_LOG_ERROR = 16
AVBIN_LOG_WARNING = 24
AVBIN_LOG_INFO = 32
AVBIN_LOG_VERBOSE = 40
AVBIN_LOG_DEBUG = 48
AVbinLogLevel = ctypes.c_int

av = libutil.load_library('avbin', 'libavbin', 11)

av.avbin_open_filename.restype = ctypes.c_void_p
av.avbin_open_filename.argtypes = [ctypes.c_char_p]

av.avbin_file_info.restype = ctypes.c_int
av.avbin_file_info.argtypes = [ctypes.c_void_p, ctypes.POINTER(AVbinFileInfo)]

av.avbin_stream_info.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                 ctypes.POINTER(AVbinstream8)]

av.avbin_set_log_level.restype = ctypes.c_int
av.avbin_set_log_level.argtypes = [AVbinLogLevel]

av.avbin_init()
av.avbin_set_log_level(AVBIN_LOG_QUIET)


def get_all_stream_info(file, fileInfo):
    """
    Returns all stream information from the AVbinFileInfo structure as
    a dictionary.
    file - The AVbin file handle
    fileInfo - The AVbinFileInfo structure
    """
    all_streams = []
    for i in xrange(fileInfo.n_streams):
        stream = {}
        info = AVbinstream8()
        info.structure_size = ctypes.sizeof(info)
        av.avbin_stream_info(file, i, info)

        stream['type'] = AVBIN_STREAM_TYPE_STRING_MAPPING[info.type]

        if info.type == AVBIN_STREAM_TYPE_VIDEO:
            stream['width'] = info.u.video.width
            stream['height'] = info.u.video.height
            if info.u.video.sample_aspect_den != 0:
                stream['sample_aspect'] = info.u.video.sample_aspect_num \
                                            / info.u.video.sample_aspect_den
            else:
                stream['sample_aspect'] = None
            if info.u.video.frame_rate_den != 0:
                stream['frame_rate'] = info.u.video.frame_rate_num \
                                         / info.u.video.frame_rate_den
            else:
                stream['frame_rate'] = None
        elif info.type == AVBIN_STREAM_TYPE_AUDIO:
            for field in info.u.audio._fields_:
                key = field[0]
                stream[key] = getattr(info.u.audio, key)

        all_streams.append(stream)
    return all_streams


def process(file, config, rcontext, columns=None):
    fullpath = file.fullpath
    try:
        fileInfo = AVbinFileInfo()
        fileInfo.structure_size = ctypes.sizeof(fileInfo)

        # open the file and let avbin write its metadata to fileInfo
        file = av.avbin_open_filename(fullpath)
        av.avbin_file_info(file, ctypes.byref(fileInfo))

        # The metadata is stored as an attribute (fileInfo.attr)
        # and not as key/value pair (fileInfo['attr']). So we are
        # looking up all possible attributes here to put them in the
        # `assorted' array using getattr()
        assorted = []
        for field in fileInfo._fields_:
            # However, don't append the 'structure_size' field as
            # it's always the same and irrelevant for us (it
            # indicates the size of the C structure)
            if field[0] != 'structure_size':
                assorted.append(getattr(fileInfo, field[0]))

        all_streams = get_all_stream_info(file, fileInfo)

        # Get the information of the first video- and audiostream.
        # If there's more than one stream, the data is made
        # available in the all_streams column as structured data.

        first_video_stream = None
        first_audio_stream = None
        for stream in all_streams:
            if stream['type'] == AVBIN_STREAM_TYPE_STRING_MAPPING[AVBIN_STREAM_TYPE_VIDEO]:
                first_video_stream = stream
            elif stream['type'] == AVBIN_STREAM_TYPE_STRING_MAPPING[AVBIN_STREAM_TYPE_AUDIO]:
                first_audio_stream = stream

        if first_video_stream != None:
            # Can't iterate here because we need to maintain a
            # specific order
            assorted.append(first_video_stream['width'])
            assorted.append(first_video_stream['height'])
            assorted.append(first_video_stream['sample_aspect'])
            assorted.append(first_video_stream['frame_rate'])
        else:
            for i in xrange(AVBIN_STREAM_ACTUAL_NUMBER_OF_VIDEO_INFO_FIELDS):
                assorted.append(None)

        if first_audio_stream != None:
            assorted.append(first_audio_stream['sample_format'])
            assorted.append(first_audio_stream['sample_rate'])
            assorted.append(first_audio_stream['sample_bits'])
            assorted.append(first_audio_stream['channels'])
        else:
            for i in xrange(len(_AVbinstreamAudio8._fields_)):
                assorted.append(None)

        assorted.append(all_streams)

        # Make sure we stored exactly the same amount of columns as
        # specified!!
        assert len(assorted) == len(columns)

        # Print some data that is stored in the database if debug is true
        if config.DEBUG:
            print "\nVideo file data:"
            for i in range(0, len(assorted)):
                print "%-18s %s" % (columns[i], assorted[i])
            print

        return assorted

    except:
        traceback.print_exc(file=sys.stderr)
        # Store values in database so not the whole application crashes
        return None
