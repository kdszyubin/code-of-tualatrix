#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from Widgets import *

class HelloWorld:

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def GotKey(self, widget, key, mods):
        new = gtk.accelerator_name (key, mods)
        for mod in KeyModifier:
            if "%s_L" % mod in new:
                new = new.replace ("%s_L" % mod, "<%s>" % mod)
            if "%s_R" % mod in new:
                new = new.replace ("%s_R" % mod, "<%s>" % mod)

        widget.destroy()
        self.FilterValueCheck.set_active(True)
        self.FilterEntry.set_text(new)

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(10)
    
        grabber = KeyGrabber(label = "Grab key combination")
        grabber.hide()
        grabber.set_no_show_all(True)
        grabber.connect('changed', self.GotKey)
        grabber.begin_key_grab(None)
    
        self.window.add(grabber)
    
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
