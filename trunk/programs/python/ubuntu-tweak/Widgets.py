#!/usr/bin/env python

# Ubuntu Tweak - PyGTK based desktop configure tool
#
# Copyright (C) 2007-2008 TualatriX <tualatrix@gmail.com>
#
# Ubuntu Tweak is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ubuntu Tweak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import pygtk
pygtk.require("2.0")
import gtk
from Settings import BoolSetting

class GconfCheckButton(gtk.CheckButton, BoolSetting):
	def __init__(self, label, key):
		gtk.CheckButton.__init__(self)
		BoolSetting.__init__(self, key)

		self.set_label(label)
		self.set_active(self.get_bool())

		self.client.notify_add(key, self.value_changed)
		self.connect("toggled", self.button_toggled)

	def value_changed(self, client, id, entry, data = None):
		self.set_active(self.get_bool())

	def button_toggled(self, widget, data = None):
		self.client.set_bool(self.key, self.get_active())

class CGconfCheckButton(GconfCheckButton):
	def __init__(self, label, key, mediator):
		GconfCheckButton.__init__(self, label, key)

		self.mediator = mediator

		self.connect("toggled", self.button_state_change)

	def button_state_change(self, widget, data = None):
		self.mediator.colleague_changed()

class Mediator:
	def colleague_changed(self):
		pass

class ItemBox(gtk.VBox):
	"""The itembox used to pack a set of widgets with a markup title"""
	def __init__(self, title, widgets = None):
		gtk.VBox.__init__(self)
		self.set_border_width(5)
		
		if title:
			label = gtk.Label()
			label.set_markup(title)
			label.set_alignment(0, 0)
			self.pack_start(label, False, False, 0)

		hbox = gtk.HBox(False, 5)
		hbox.set_border_width(5)
		self.pack_start(hbox, True, False, 0)

		label = gtk.Label(" ")
		hbox.pack_start(label, False, False, 0)

		self.vbox = gtk.VBox(False, 0)
		hbox.pack_start(self.vbox, True, True, 0)

		if widgets:
			if len(widgets) < 2:
				if type(widgets[0]) == GconfCheckButton:
					self.vbox.pack_start(widgets[0], False, False, 0)
				else:
					self.add(widgets[0])
			else:
				for widget in widgets:
					self.vbox.pack_start(widget, False, False, 0)

class EntryBox(gtk.HBox):
	def __init__(self, label, text):
		gtk.HBox.__init__(self)

		label = gtk.Label(label)
                self.pack_start(label, False, False,10)
                entry = gtk.Entry()
		if text: entry.set_text(text)
                entry.set_editable(False)
		entry.set_size_request(300, -1)
                self.pack_end(entry, False, False, 0)

class HScaleBox(gtk.HBox):

	def hscale_value_changed_cb(self, widget, data = None):
		client = gconf.client_get_default()
		value = client.get(data)
		if value.type == gconf.VALUE_INT:
			client.set_int(data, int(widget.get_value()))
		elif value.type == gconf.VALUE_FLOAT:
			client.set_float(data, widget.get_value())

	def __init__(self, label, min, max, key, digits = 0):
		gtk.HBox.__init__(self)
		self.pack_start(gtk.Label(label), False, False, 0)
		
		hscale = gtk.HScale()
		hscale.set_size_request(150, -1)
		hscale.set_range(min, max)
		hscale.set_digits(digits)
		hscale.set_value_pos(gtk.POS_RIGHT)
		self.pack_end(hscale, False, False, 0)
		hscale.connect("value-changed", self.hscale_value_changed_cb, key)

		client = gconf.client_get_default()
		value = client.get(key)

		if value:
			if value.type == gconf.VALUE_INT:
				hscale.set_value(client.get_int(key))
			elif value.type == gconf.VALUE_FLOAT:
				hscale.set_value(client.get_float(key))


class ComboboxItem(gtk.HBox):

	def __init__(self, label, texts, values, key):
		gtk.HBox.__init__(self)
		self.pack_start(gtk.Label(label), False, False, 0)	

		combobox = gtk.combo_box_new_text()
		combobox.texts = texts
		combobox.values = values
		combobox.connect("changed", self.value_changed_cb, key)
		self.pack_end(combobox, False, False, 0)

		for element in texts:
			combobox.append_text(element)

		client = gconf.client_get_default()

		if client.get_string(key) in values:
			combobox.set_active(values.index(client.get_string(key)))
	def value_changed_cb(self, widget, data = None):
		client = gconf.client_get_default()
		text = widget.get_active_text()
		client.set_string(data, widget.values[widget.texts.index(text)]) 

class AboutBlank:
	pass