#!/usr/bin/env python
# coding: utf-8

import gtk
import gconf
from Widgets import *
from Utility import ManyTest, Test
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class Bool(gtk.VBox):
	def __init__(self, label):
		gtk.VBox.__init__(self)

		self.Widget = gtk.HBox ()
		self.pack_start(self.Widget)

		self.CheckButton = gtk.CheckButton ()
		label = gtk.Label (label)
		self.align = gtk.Alignment ()
		self.align.add (label)
		self.buttonAlign = gtk.Alignment (0, 0.5)
		self.buttonAlign.set_padding (0, 0, 0, 10)
		self.buttonAlign.add (self.CheckButton)
		self.Widget.pack_start (self.align, True, True)
		self.Widget.pack_start (self.buttonAlign, False, False)

		self.show_all()

def ComboboxItem(texts):
	comboxbox = gtk.combo_box_new_text()

	for element in texts:
		comboxbox.append_text(element)

	return comboxbox

class BoolAndInt(gtk.VBox):
	def __init__(self, label):
		gtk.VBox.__init__(self)

		self.Widget = gtk.HBox ()
		self.pack_start(self.Widget)

		self.CheckButton = gtk.CheckButton (label)
		self.align = gtk.Alignment (0, 0.5)
		self.align.add (self.CheckButton)

		self.scale = gtk.HScale()
		self.buttonAlign = gtk.Alignment (0, 0.5)
		self.buttonAlign.set_padding (0, 0, 0, 10)
		self.buttonAlign.add (self.scale)
		self.Widget.pack_start (self.align, True, True)
		self.Widget.pack_start (self.buttonAlign, False, False)

		self.show_all()

if __name__ == "__main__":
	win = gtk.Window()

	win.connect('destroy', lambda *w: gtk.main_quit())
	win.set_position(gtk.WIN_POS_CENTER)

	vbox = gtk.VBox(False, 5)
	win.add(vbox)

	vbox.pack_start(GconfCombobox("/apps/gwd/mouse_wheel_action", ["None", "Roll up"], ["none", "shade"]).combobox)
	
	win.show_all()

	gtk.main()
