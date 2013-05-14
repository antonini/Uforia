#!/usr/bin/env python

# Load basic Python modules
import os
import multiprocessing
import imp
import curses
import sys
import platform
import traceback
import site
import subprocess
import ctypes
import recursive
import hashlib

# Loading of Uforia modules is deferred until run() is called
config = None
File = None
magic = None
modules = None
database = None


def dbworker(dbqueue, db=None):
    """
    Receives new argument lists from the database queue and writes them
    to the database. The worker will continue until it receives a table
    with the name "No more tasks" (the sentinel) in the argument list. Upon
    receiving the sentinel, it will send a commit to write out all
    outstanding I/O to the database.

    dbqueue - The database queue, a multiprocessing.JoinableQueue
    db - Optionally use another database object
    """
    if db == None:
        db = database.Database(config)

    while True:
        table, hashid, columns, values = dbqueue.get()
        if table != "No more tasks":
            db.store(table, hashid, columns, values)
            dbqueue.task_done()
        else:
            break

    db.connection.commit()
    dbqueue.task_done()
    db.connection.close()


def monitorworker(monitorqueue):
    """
    Starts the monitor display for the curses console.

    monitorqueue - The multiprocessing.JoinableQueue that emits the
        currently examined file
    """
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    while True:
        val = monitorqueue.get()
        if val != None:
            stdscr.clear()
            stdscr.addstr(0, 0, "=== Uforia ===")
            stdscr.addstr(2, 0, "Examining:")
            stdscr.addstr(2, 20, str(val))
            if config.DEBUG:
                stdscr.addstr(24, 0, "Warning: console output will be severely mangled with debug enabled.")
            stdscr.clrtoeol()
            stdscr.refresh()
            monitorqueue.task_done()
        else:
            break

    monitorqueue.task_done()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


def write_to_mimetypes_table(table, columns, values, db=None):
    """
    Method that writes to database

    table - the database table
    columns - the database columns
    values - the values for in the columns
    db - Optionally use another database object
    """
    if db == None:
        db = database.Database(config)

    db.store_mimetype_values(table, columns, values)

    db.connection.commit()
    db.connection.close()


def file_scanner(dir, consumers, dbqueue, monitorqueue, uforiamodules,
                 config, rcontext):
    """
    Walks through the specified directory tree to find all files. Each
    file is passed through file_processor, which is called asynchronously
    through the multiprocessing pool (consumers).

    dir - The path to search
    consumers - The multiprocessing.Pool which will carry out the
        file processing task
    dbqueue - The database queue, passed to file_processor
    uforiamodules - Loaded uforia modules, passed to file_processor
    """
    try:
        if config.DEBUG:
            print("Starting in directory " + dir + "...")
            print("Starting filescanner...")
        hashid = rcontext.STARTING_HASHID
        filelist = []
        for root, dirs, files in os.walk(dir, topdown=True, followlinks=False):
            for name in files:
                fullpath = os.path.join(root, name)
                filelist.append((fullpath, hashid))
                hashid += 1
        rcontext.STARTING_HASHID = hashid
        try:
            consumermap = [(item, dbqueue, monitorqueue, uforiamodules, config, rcontext) for item in filelist]
            result = consumers.map_async(file_processor, consumermap)

            # Wait while file_processor is busy in order to catch a possible KeyboardInterrupt.
            #
            # An infinite float was used;we can't use get() with no arguments as it will
            # ignore the exception.
            result.get(float('inf'))
            consumers.close()
            consumers.join()
        except KeyboardInterrupt:
            consumers.terminate()
    except:
        traceback.print_exc(file=sys.stderr)
        raise


def invoke_modules(dbqueue, uforiamodules, hashid, file, config, rcontext):
    """
    Loads all Uforia modules in the current process and invokes them.
    Only modules that apply to the current MIME-type are loaded.
    The result of the module's process method will be put to the
    database queue.

    dbqueue - The database queue, a multiprocessing.JoinableQueue
    uforiamodules - The uforia module objects from modulescanner
    hashid - The hash id of the currently processed file
    file - The file currently being processed
    """
    modules = uforiamodules.get_modules_for_mimetype(file.mtype)
    nr_handlers = 0
    for module in modules:
        if module.is_mime_handler:
            nr_handlers += 1

    if nr_handlers == 0:
        if config.DEBUG:
            print "No modules found to handle MIME-type " + file.mtype + ", skipping additional file parsing..."
    else:
        try:
            modules = uforiamodules.get_modules_for_mimetype(file.mtype)
            if config.DEBUG:
                print "Setting up " + str(nr_handlers) + " module workers..."

            for module in modules:
                try:
                    # If module fails catch it's exception and continue running Uforia.
                    module.load_sources()
                    processresult = None
                    if module.is_mime_handler:
                        processresult = module.pymodule.process(file.fullpath, config, rcontext, columns=module.columnnames)
                    if processresult != None:
                        dbqueue.put((module.md5_tablename, hashid, module.columnnames, processresult))
                except:
                    traceback.print_exc(file=sys.stderr)
        except:
            traceback.print_exc(file=sys.stderr)
            raise


def file_processor((item, dbqueue, monitorqueue, uforiamodules, config,
                    rcontext)):
    """
    Process a file item and export its information to the database
    queue. Also calls invoke_modules() if modules are enabled in the
    configuration.

    item - Tuple containing the fullpath and hashid of the file
    dbqueue - The database queue, a multiprocessing.JoinableQueue
    monitorqueue - The monitoring queue to show information about the
        current file
    uforiamodules - The uforia module objects from modulescanner
    """
    try:
        multiprocessing.current_process().daemon = False
        fullpath, hashid = item
        file = File.File(fullpath, config, magic)
        if config.OUTPUT:
            monitorqueue.put(fullpath)
        try:
            if config.DEBUG:
                print("Exporting basic hashes and metadata to database.")
            columns = ('fullpath', 'name', 'size', 'owner', 'group', 'perm', 'mtime', 'atime', 'ctime', 'md5', 'sha1', 'sha256', 'ftype', 'mtype', 'btype')
            if rcontext.SPOOFSTARTDIR != None:
                fullpath = rcontext.SPOOFSTARTDIR + os.path.sep + os.path.relpath(file.fullpath, config.STARTDIR)
            else:
                fullpath = file.fullpath
            fullpath = os.path.normpath(fullpath)
            values = (fullpath, file.name, file.size, file.owner, file.group, file.perm, file.mtime, file.atime, file.ctime, file.md5, file.sha1, file.sha256, file.ftype, file.mtype, file.btype)
            dbqueue.put(('files', hashid, columns, values))
        except:
            traceback.print_exc(file=sys.stderr)
            raise
        if not config.ENABLEMODULES:
            if config.DEBUG:
                print("Additional module parsing disabled by config, skipping...")
        else:
            invoke_modules(dbqueue, uforiamodules, hashid, file, config, rcontext)
    except:
        traceback.print_exc(file=sys.stderr)
        raise


def fill_mimetypes_table(dbqueue, uforiamodules):
    """
    Fills the supported_mimetypes table with all available mime-types
    """
    if config.DEBUG:
        print "Getting available mimetypes..."
    mime_types = uforiamodules.get_all_supported_mimetypes_with_modules()
    for mime_type in mime_types:
        write_to_mimetypes_table('supported_mimetypes', ["mime_type", "modules"], [mime_type, mime_types[mime_type]])


def run():
    """
    Starts Uforia.

    Sets up the database, modules, all background processes and then
    invokes the file_scanner.
    """
    print("Uforia starting...")

    if config.DEBUG:
        print("Initializing " + str(config.DBCONN) + " " + config.DBTYPE + " database worker thread(s)...")

    manager = multiprocessing.Manager()
    dbqueue = manager.JoinableQueue()
    dbworkers = []

    # Create database tables
    db = database.Database(config)
    if not rcontext.RECURSIVE:
        db.setup_main_table()
        db.setup_mimetypes_table()

    for i in range(config.DBCONN):
        dbworkers.append(multiprocessing.Process(target=dbworker, args=(dbqueue,)))
        dbworkers[i].daemon = True
        dbworkers[i].start()
    if config.ENABLEMODULES:
        if config.DEBUG:
            print("Detecting available modules...")
        uforiamodules = modules.Modules(config, db, rcontext)
        if not rcontext.RECURSIVE:
            fill_mimetypes_table(dbqueue, uforiamodules)
    else:
        uforiamodules = ''
    del db
    monitorqueue = None
    if config.OUTPUT:
        monitorqueue = manager.JoinableQueue()
        monitorthread = multiprocessing.Process(target=monitorworker, args=(monitorqueue,))
        monitorthread.daemon = True
        monitorthread.start()
    if config.DEBUG:
        print("Setting up " + str(config.CONSUMERS) + " consumer(s)...")
    consumers = multiprocessing.Pool(processes=config.CONSUMERS)
    if config.DEBUG:
        print("Starting producer...")
    if os.path.exists(config.STARTDIR):
        file_scanner(config.STARTDIR, consumers, dbqueue, monitorqueue, uforiamodules, config, rcontext)
    else:
        print("The pathname " + config.STARTDIR + " does not exist, stopping...")
    for i in range(config.DBCONN):
        dbqueue.put(('No more tasks', '', '', ''))
    dbqueue.join()
    if config.OUTPUT:
        monitorqueue.put(None)
        monitorqueue.join()
    print("\nUforia completed...\n")


class _Dummy(object):
    pass


def config_as_pickleable(config):
    """
    Converts config (which has the `module' type) to a pickleable object.
    """
    values = config.__dict__
    newConfig = _Dummy()
    for key, value in values.items():
        if not key.startswith('__'):
            setattr(newConfig, key, value)
    return newConfig


def setup_library_paths():
    """
    Setup the PATH environmental variable so that python libraries, .pyd, .so and
    .dll files can be loaded without intervention. This does not work for Linux
    shared object files loaded with ctypes.
    """
    architecture = 'x86_64' if ctypes.sizeof(ctypes.c_voidp) == 8 else 'x86'
    operatingSystem = platform.system()

    # Needs to be loaded first, otherwise system-wide libraries are preferred
    sys.path.insert(0, "./libraries")
    sys.path.append("./libraries/PIL/bin-{0}-{1}".format(architecture, operatingSystem))
    if platform.system() == 'Windows':
        # sys.path.append is not reliable for this thing
        os.environ['PATH'] += ";./libraries/windows-deps"

setup_library_paths()


# Fixes crash-on-exit bugs on Windows by loading it before libmagic
import libxmp

config = imp.load_source('config', 'include/default_config.py')
try:
    config = imp.load_source('config', 'include/config.py')
except:
    print("< WARNING! > Config file not found or not configured correctly, loading default config.")
File = imp.load_source('File', 'include/File.py')
magic = imp.load_source('magic', 'include/magic.py')
modules = imp.load_source('modulescanner', 'include/modulescanner.py')
database = imp.load_source(config.DBTYPE, config.DATABASEDIR + config.DBTYPE + ".py")

config = config_as_pickleable(config)
config.UFORIA_RUNNING_VERSION = 'Uforia'
rcontext = recursive.RecursionContext()

if __name__ == "__main__":
    run()
