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
from UserList import UserList

(
	COLUMN_TITLE,
	COLUMN_NUM,
	COLUMN_PATH,
) = range(3)

class ExistBook(UserList):
        def __init__(self, path):
                UserList.__init__(self)
                self.createbookdir(path)

        def createbookdir(self, path):
                for file in os.listdir(path):
                        hasbooks = glob.glob(path + "/" + file + "/*.bok")
                        if not hasbooks:
                                file = path + "/" + file
                                if os.path.isdir(file):
                                        self.createbookdir(file)
                        else:
                                self.extend(hasbooks)

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

		main_hbox = gtk.HBox(False, 5)
		main_hbox.show()
		self.pack_start(main_hbox)

		self.wordlist = WordList()
		self.wordlist.show()

		treeview = BookList(self.wordlist)
		treeview.show()

		vbox = gtk.VBox(False, 10)
		vbox.show()
		main_hbox.pack_start(vbox, False, False, 0)

		sw = gtk.ScrolledWindow()
##		sw.set_size_request(200, -1)
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)
		sw.add(treeview)

		hbox = gtk.HBox(False, 5)
		hbox.show()
		vbox.pack_start(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_ADD)
		button.connect("clicked", self.on_add_book_clicked, treeview)
		button.show()
		hbox.pack_start(button)

		button = gtk.Button(stock = gtk.STOCK_REMOVE)
		button.show()
		hbox.pack_start(button)

		vbox = gtk.VBox(False, 10)
		vbox.show()
		main_hbox.pack_start(vbox)

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		hbox = gtk.HBox(False, 5)
		hbox.show()
		vbox.pack_start(hbox, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.show()
		hbox.pack_start(self.entry)

		button = gtk.Button(stock = gtk.STOCK_ADD)
		button.connect("clicked", self.on_add_word_clicked, self.wordlist)
		button.show()
		hbox.pack_start(button, False, False, 0)

		sw.add(self.wordlist)

	def on_add_word_clicked(self, widget, data = None):
		word_add = self.entry.get_text()
		print word_add

		books = ExistBook("/usr/share/reciteword/books") 
		Find = True 
		for book in books:
			while Find:
				for word in file(book):
					if word.find("[W]" + word_add + "[T]") >= 0:
						Find = False 
						print "%d" % (books.index(book) + 1)
						break
			else:
				break
		

	def on_add_book_clicked(self, widget, data = None):
		dialog = gtk.Dialog("添加生词库", None, 
				gtk.DIALOG_MODAL, 
				(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
				gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

		title_label = gtk.Label("书名:")
		title_label.show()
		dialog.vbox.pack_start(title_label)
		
		title_entry = gtk.Entry()
		title_entry.show()
		dialog.vbox.pack_start(title_entry)

		file_label = gtk.Label("文件名:")
		file_label.show()
		dialog.vbox.pack_start(file_label)
		
		file_entry = gtk.Entry()
		file_entry.show()
		dialog.vbox.pack_start(file_entry)

		response = dialog.run()
		if response == gtk.RESPONSE_ACCEPT:
			book_title = title_entry.get_text()
			book_path = os.path.join(os.path.expanduser("~"), ".myword/books/", file_entry.get_text())+".bok"

			newbook = DictFile(book_path)
			newbook.INFO = {}
			newbook.INFO['FILE'] = book_path
			newbook.INFO['TITLE'] = book_title
			newbook.INFO['NUM'] = '0'
			newbook.INFO['AUTHOR'] = 'TualatriX'
			newbook.INFO['OTHER'] = 'http://imtx.cn'
			newbook.save()

			model = data.get_model()
			iter = model.append()
			model.set(iter,
				COLUMN_TITLE, book_title,
				COLUMN_NUM, 0,
				COLUMN_PATH, book_path)

		dialog.destroy()

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
