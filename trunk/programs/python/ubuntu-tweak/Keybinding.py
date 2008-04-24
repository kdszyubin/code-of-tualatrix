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
import os
import gconf
import gettext
import gobject

from Constants import *
from Widgets import TweakPage
from Factory import Factory

gettext.install(App, unicode = True)

(
		COLUMN_ID,
		COLUMN_TITLE,
		COLUMN_ICON,
		COLUMN_COMMAND,
		COLUMN_KEY,
		COLUMN_EDITABLE,
) = range(6)

class Keybinding(TweakPage):
	"""Setting the command of keybinding"""

	def __init__(self):
		TweakPage.__init__(self)
		gtk.VBox.__init__(self)

		self.set_title(_("Set your keybinding of commands"))
		self.set_description(_("With the keybinding of commands, you can run applications more quickly"))

		treeview = self.create_treeview()

		self.pack_start(treeview)
	
	def create_treeview(self):
		treeview = gtk.TreeView()

		model = self.__create_model()

		treeview.set_model(model)

		self.__add_columns(treeview)

		return treeview

	def __create_model(self):
		model = gtk.ListStore(
				gobject.TYPE_INT,
				gobject.TYPE_STRING,
				gtk.gdk.Pixbuf,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_BOOLEAN,
				)

		client = gconf.client_get_default()

		for id in range(12):
			iter = model.append()
			icontheme = gtk.icon_theme_get_default()
			id = id + 1

			title = _("Command %d") % id
			command = client.get_string("/apps/metacity/keybinding_commands/command_%d" % id)
			key = client.get_string("/apps/metacity/global_keybindings/run_command_%d" % id)

			if not command: command = _("None")
			icon = icontheme.lookup_icon(command, 32, gtk.ICON_LOOKUP_NO_SVG)
			if icon: icon = icon.load_icon()

			model.set(iter,
					COLUMN_ID, id,
					COLUMN_TITLE, title,
					COLUMN_ICON, icon,
					COLUMN_COMMAND, command,
					COLUMN_KEY, key,
					COLUMN_EDITABLE, True)

		return model

	def __add_columns(self, treeview):
		model = treeview.get_model()

		column = gtk.TreeViewColumn(_("Title"), gtk.CellRendererText(), text = COLUMN_TITLE)
		column.set_fixed_width(32)
		treeview.append_column(column)

		column = gtk.TreeViewColumn(_("Command"))

		renderer = gtk.CellRendererPixbuf()
		column.pack_start(renderer, False)
		column.set_attributes(renderer, pixbuf = COLUMN_ICON)

		renderer = gtk.CellRendererText()
		renderer.connect("edited", self.on_cell_edited, model)
		renderer.set_data("type", "command")
		column.pack_start(renderer, True)
		#column.set_attributes(renderer, text = COLUMN_COMMAND)
		column.set_attributes(renderer, text = COLUMN_COMMAND, editable = COLUMN_EDITABLE)
#		column = gtk.TreeViewColumn(_("Command"), renderer, text = COLUMN_COMMAND, editable = COLUMN_EDITABLE)
		treeview.append_column(column)
	
		renderer = gtk.CellRendererText()
		renderer.connect("edited", self.on_cell_edited, model)
		renderer.set_data("type", "key")
		column = gtk.TreeViewColumn(_("Key"), renderer, text = COLUMN_KEY, editable = COLUMN_EDITABLE)
		treeview.append_column(column)

	def on_cell_edited(self, cell, path_string, new_text, model):
		iter = model.get_iter_from_string(path_string)

		client = gconf.client_get_default()
		column = cell.get_data("id")

		type = cell.get_data("type")
		id = model.get_value(iter, COLUMN_ID)

		if type == "command":
			old = model.get_value(iter, COLUMN_COMMAND)
			if old != new_text:
				client.set_string("/apps/metacity/keybinding_commands/command_%d" % id, new_text)
				if new_text:
					icontheme = gtk.icon_theme_get_default()
					icon = icontheme.lookup_icon(new_text, 32, gtk.ICON_LOOKUP_NO_SVG)
					if icon: icon = icon.load_icon()

					model.set_value(iter, COLUMN_ICON, icon)
					model.set_value(iter, COLUMN_COMMAND, new_text)
				else:
					model.set_value(iter, COLUMN_ICON, None)
					model.set_value(iter, COLUMN_COMMAND, _("None"))
		else:
			old = model.get_value(iter, COLUMN_KEY)
			if old != new_text:
				if new_text:
					client.set_string("/apps/metacity/global_keybindings/run_command_%d" % id, new_text)
					model.set_value(iter, COLUMN_KEY, new_text)
				else:
					client.set_string("/apps/metacity/global_keybindings/run_command_%d" % id, "disabled")
					model.set_value(iter, COLUMN_KEY, _("disabled"))

if __name__ == "__main__":
	from Utility import Test
	Test(Keybinding)
