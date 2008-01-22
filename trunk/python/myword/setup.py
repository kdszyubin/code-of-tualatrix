#!/usr/bin/env python

import os
import sys
from stat import *
from distutils.core import setup
from distutils.command.install import install as _install
from distutils.command.install_data import install_data as _install_data

INSTALLED_FILES = "installed_files"

class install (_install):
    def run (self):
        _install.run (self)
        outputs = self.get_outputs ()
        length = 0
        if self.root:
            length += len (self.root)
        if self.prefix:
            length += len (self.prefix)
        if length:
            for counter in xrange (len (outputs)):
                outputs[counter] = outputs[counter][length:]
        data = "\n".join (outputs)
        try:
            file = open (INSTALLED_FILES, "w")
        except:
            self.warn ("Could not write installed files list %s" % \
                       INSTALLED_FILES)
            return 
        file.write (data)
        file.close ()

class install_data (_install_data):
    def run (self):
        def chmod_data_file (file):
            try:
                os.chmod (file, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)
            except:
                self.warn ("Could not chmod data file %s" % file)
        _install_data.run (self)
        map (chmod_data_file, self.get_outputs ())

class uninstall (_install):

    def run (self):
        try:
            file = open (INSTALLED_FILES, "r")
        except:
            self.warn ("Could not read installed files list %s" % \
                       INSTALLED_FILES)
            return 
        files = file.readlines ()
        file.close ()
        prepend = ""
        if self.root:
            prepend += self.root
        if self.prefix:
            prepend += self.prefix
        if len (prepend):
            for counter in xrange (len (files)):
                files[counter] = prepend + files[counter].rstrip ()
        for file in files:
            print "Uninstalling %s" % file
            try:
                os.unlink (file)
            except:
                self.warn ("Could not remove file %s" % file)

ops = ("install", "sdist", "uninstall", "clean")

if len (sys.argv) < 2 or sys.argv[1] not in ops:
    print "Please specify operation : %s" % " | ".join (ops)
    raise SystemExit

srcdir = os.path.join (os.path.realpath ("."), "src")
src = map(lambda i: "src/%s" % i, filter(lambda i: i[-2:] == "py", os.listdir (srcdir)))

bookdir = os.path.join (os.path.realpath ("."), "src/books")
books = map(lambda i: "src/boook/%s" % i, filter(lambda i: i[-3:] == "png", os.listdir(bookdir)))

data_files = [
                ("/usr/share/applications", ["myword.desktop"]),
		("/usr/share/myword", src),
		("/usr/share/myword/sound", ["src/sound"]),
                ("/usr/share/myword/books", ["src/books"]),
                ("/usr/bin", ["myword"]),
             ]

setup(
	name		= "myword",
	version		= "0.9.5",
	description	= "PyGTK based word-recite application",
	author		= "TualatriX",
	author_email	= "tualatrix@gmail.com",
	url		= "http://imtx.cn",
	license		= "GPL",
	data_files	= data_files,
        cmdclass         = {"uninstall" : uninstall,
                            "install" : install,
                            "install_data" : install_data}
)
