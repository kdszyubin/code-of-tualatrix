#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import gobject

from dictfile import DictFile
from reciterecord import ReciteRecord

class FirstRecite(gtk.VBox):
	def __init__(self, book):
		gtk.VBox.__init__(self)
		self.book = book
		self.show()

		# Stage 1, Confirm WordList
		self.wordlist = self.create_wordlist()
		self.pack_start(self.wordlist)

		# Stage 2, Word Preview
		self.preview = self.create_wordpreview()
		self.pack_start(self.preview)
		
	def create_wordlist(self):
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

	def create_wordpreview(self):
		vbox = gtk.VBox(False, 0)

		en = gtk.Label("EN")
		en.show()
		vbox.pack_start(en)
		cn = gtk.Label("CN")
		cn.show()
		vbox.pack_start(cn)

		return vbox

	def button_clicked_cb(self, widget, data = None):
		self.wordlist.hide()
		self.preview.show()

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

		return listview, record

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
