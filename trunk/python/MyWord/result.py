#!/usr/bin/env python
# coding: utf-8

import gtk
import gobject
import os

from dictfile import DictFile

class Result(gtk.VBox):

	def __init__(self):
		gtk.VBox.__init__(self, False, 10)

		listview = self.create_listview()

		self.pack_start(listview)

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
		column = gtk.TreeViewColumn("书名", renderer, text = 0)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = 1)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("还需要复习次数", renderer, text = 1)

		selection = listview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed)

		return listview	

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("Result")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = Result()
        win.add(vbox)

        win.show_all()
	gtk.main()
