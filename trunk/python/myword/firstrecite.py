#!/usr/bin/env python
# coding: utf-8

# Myword - Python based word recite application
#
# Copyright (C) 2008 TualatriX <tualatrix@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import gtk
import gobject
import cPickle as pickle

from dictfile import DictFile
from reciterecord import ReciteRecord
from playsound import read, play
from widgets import show_info
from widgets import WordTest

class FirstRecite(gtk.VBox):
	def __init__(self, book):
		gtk.VBox.__init__(self)

		self.book = book
		self.rr = None

		self.status = gtk.Label()
		self.status.show()
		self.status.set_markup('<span size="xx-large">单词初记-浏览</span>')
		self.pack_start(self.status, False, False, 10)

		# Stage 1, Confirm WordList
		self.preview = self.create_preview()
		self.pack_start(self.preview, True, True, 10)

		# Stage 2, test function
		self.wordtest = WordTest(self.rr,
					"first",
					self.preview,
					self.status,
					self.create_model)
		self.pack_start(self.wordtest, False, False, 10)

	def create_preview(self):
		hpaned = gtk.HPaned()
		hpaned.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_size_request(280, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack1(sw)

		listview = self.create_listview()
		sw.add(listview)

		vbox = gtk.VBox(False, 5)
		vbox.show()

		hbox = gtk.HBox(False, 0)
		hbox.show()
		vbox.pack_start(hbox, False, False, 0)

		label = gtk.Label("你要背诵几个单词?")
		label.show()
		hbox.pack_start(label, False, False, 0)

		spinbutton = gtk.SpinButton(gtk.Adjustment(25, 5, 100, 1, 1, 1))
		spinbutton.connect("value-changed", self.value_changed_cb)
		spinbutton.show()
		hbox.pack_end(spinbutton, False, False, 0)

		button = gtk.Button("确定")
		button.show()
		button.connect("clicked", self.start_clicked_cb)
		vbox.pack_end(button, False, False, 0)

		button = gtk.Button("返回")
		button.show()
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

		return hpaned

	def create_listview(self):
		listview = gtk.TreeView()
		listview.show()

		self.model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		listview.set_model(self.model)

		if self.book:
			self.create_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词", renderer, text = 0)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("中文解释", renderer, text = 1)
		listview.append_column(column)

		selection = listview.get_selection()
		selection.set_mode(gtk.SELECTION_BROWSE)
		selection.connect("changed", self.selection_changed)

		return listview

	def create_model(self, count = 25):
		self.model.clear()
		self.rr = ReciteRecord(self.book, count)

		for word in self.rr.words:
			iter = self.model.append()
			self.model.set(iter,
				0, word,
				1, self.rr.dict[word].strip())

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			read(model.get_value(iter, 0))

	def value_changed_cb(self, widget, data = None):
		self.model.clear()
		self.create_model(widget.get_value())

	def start_clicked_cb(self, widget, data = None):
		self.wordtest.create_test(self.rr)
		self.preview.hide()
		self.status.set_markup('<span size="xx-large">单词初记-测试</span>')
		self.wordtest.entry.grab_focus()
		self.wordtest.show()

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
