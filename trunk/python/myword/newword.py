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

import gtk
import gobject
import sys
import os
import glob
from dictfile import DictFile
from playsound import read

(
	COLUMN_TITLE,
	COLUMN_NUM,
	COLUMN_PATH,
) = range(3)

class BookList(gtk.TreeView):
	"""the new word book list"""
	def __init__(self, list = None):
		gtk.TreeView.__init__(self)

		model = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)

		self.set_model(model)
		self.__create_model(model)

		self.__add_columns()
		self.set_rules_hint(True)
		self.set_size_request(180, -1)
		self.expand_all()

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed, list)

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		book = model.get_value(iter, COLUMN_PATH)
		if book:
			data.update_list(book)

	def __create_model(self, model):
		booksdir = os.path.join(os.path.expanduser("~"), ".myword/books")
		for item in os.listdir(booksdir):
			fullname = os.path.join(booksdir, item)
			dict = DictFile(fullname, light = True)
			iter = model.append()
			model.set(iter,
				COLUMN_TITLE, dict.INFO["TITLE"],
				COLUMN_NUM, dict.INFO["NUM"],
				COLUMN_PATH, fullname)

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		self.append_column(column)

class WordList(gtk.TreeView):
	"""Show a full list of a book"""
	def __init__(self):
		gtk.TreeView.__init__(self)

		self.model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		self.set_model(self.model)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词", renderer, text = 0)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("中文解释", renderer, text = 1)
		self.append_column(column)

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_BROWSE)
		selection.connect("changed", self.selection_changed)

	def update_list(self, book):
		self.model.clear()
		self.dict = DictFile(book)

		for word in self.dict.keys():
			iter = self.model.append()
			self.model.set(iter,
				0, word,
				1, self.dict[word].strip())

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			read(model.get_value(iter, 0))

class NewWord(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 10)

		self.book = None

		hpaned = gtk.HPaned()
		hpaned.show()
		self.pack_start(hpaned)

		self.wordlist = WordList()
		self.wordlist.show()

		treeview = BookList(self.wordlist)
		treeview.show()

		vpaned = gtk.VPaned()
		vpaned.show()
		vpaned.pack1(treeview)

		button = gtk.Button("新建生词库")
		button.show()
		vpaned.pack2(button)

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack1(sw)
		sw.add(vpaned)

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack2(sw)

		sw.add(self.wordlist)

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("NewWord")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = NewWord()
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
