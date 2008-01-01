#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import gobject

from dictfile import DictFile
from reciterecord import ReciteRecord
from readword import readword, typeword, delword

class FirstRecite(gtk.VBox):
	def __init__(self, book):
		gtk.VBox.__init__(self)
		self.book = book
		self.show()

		# Stage 1, Confirm WordList
		self.preview = self.create_preview()
		self.pack_start(self.preview)

		# Stage 2, te
		self.wordtest = self.create_test()
		self.pack_start(self.wordtest)
		
	def create_preview(self):
		hpaned = gtk.HPaned()
		hpaned.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_size_request(200, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		listview, self.rr = self.create_listview()
		sw.add(listview)

		hpaned.pack1(sw)

		vbox = gtk.VBox(False, 10)
		vbox.show()

		button = gtk.Button("确定")
		button.show()
		button.connect("clicked", self.button_clicked_cb)
		vbox.pack_end(button, False, False, 0)

		button = gtk.Button("返回")
		button.show()
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

		return hpaned

	def create_test(self):
		vbox = gtk.VBox(False, 0)

		self.cn = gtk.Label(self.rr.dict[self.rr.words[0]])
		self.cn.set_alignment(0, 0)
		self.cn.show()
		vbox.pack_start(self.cn, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.connect("activate", self.check_cb)
		self.entry.connect("insert-text", self.type_cb)
		self.entry.connect("backspace", self.backspace_cb)
		self.entry.show()
		vbox.pack_start(self.entry, False, False, 0)

		self.result = gtk.Label()
		self.result.set_alignment(0, 0)
		vbox.pack_start(self.result, False, False, 0)

		return vbox

	def type_cb(self, widget, new_text, new_text_length, position, data = None):
		typeword()

	def backspace_cb(self, widget, data = None):
		delword()

	def check_cb(self, widget, data = None):
		self.result.show()
		self.result.set_text("Hello")

	def button_clicked_cb(self, widget, data = None):
		self.preview.hide()
		self.wordtest.show()

	def create_listview(self):
		listview = gtk.TreeView()
		listview.show()

		model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		record = ReciteRecord(self.book)

		for word in record.words:
			iter = model.append()
			model.set(iter,
				0, word,
				1, record.dict[word].strip())

		listview.set_model(model)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词", renderer, text = 0)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("中文解释", renderer, text = 1)
		listview.append_column(column)

		selection = listview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed)

		return listview, record

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			readword(model.get_value(iter, 0))

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

#        vbox = FirstRecite()
        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
