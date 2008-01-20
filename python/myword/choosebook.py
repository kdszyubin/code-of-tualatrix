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
import os

from dictfile import DictFile
from reciterecord import ReciteRecord
from widgets import show_info

(
	COLUMN_TITLE,
	COLUMN_NUM,
	COLUMN_AUTHOR,
	COLUMN_BOOKPATH,
) = range(4)

(
	COLUMN_DIR,
	COLUMN_PATH
) = range(2)

class BookList(gtk.TreeView):
	"""书本列表"""
	def __init__(self, parent = None):
		gtk.TreeView.__init__(self)

		model = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)

		self.set_model(model)
		self.__add_columns()
		self.set_rules_hint(True)

	def create_list(self, dir, model):
		for item in os.listdir(dir):
			fullname = os.path.join(dir, item)
			if os.path.isdir(fullname):
				dirnamefile = os.path.join(fullname, "dirname")
				self.create_list(fullname, model)
			elif os.path.basename(fullname) != "dirname":
				dict = DictFile(fullname, light = True)
				iter = model.append()
				model.set(iter,
					COLUMN_TITLE, dict.INFO["TITLE"],
					COLUMN_NUM, dict.INFO["NUM"],
					COLUMN_AUTHOR, dict.INFO["AUTHOR"],
					COLUMN_BOOKPATH, fullname)

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		column.set_sort_column_id(COLUMN_TITLE)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		column.set_sort_column_id(COLUMN_NUM)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("作者", renderer, text = COLUMN_AUTHOR)
		self.append_column(column)

class DirList(gtk.TreeView):
	def __init__(self, dir, list = None):
		gtk.TreeView.__init__(self)

		model = gtk.TreeStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)
		iter = model.append(None)
		model.set(iter, COLUMN_DIR, "单词库")
		child_iter = model.append(iter)
		mybookdir = os.path.join(os.path.expanduser("~"),".myword/books")
		model.set(child_iter,
			COLUMN_DIR, "我的生词库",
			COLUMN_PATH, mybookdir)
		self.__create_model(mybookdir, model, iter)
		self.__create_model(dir, model, iter)

		self.set_model(model)
		self.__add_columns()
		self.set_rules_hint(True)
		self.set_size_request(180, -1)
		self.expand_all()

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed, list)
		selection.select_iter(model.iter_children(model.get_iter_first()))

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		dir = model.get_value(iter, COLUMN_PATH)
		if dir:
			list = data.get_model()
			list.clear()
			data.create_list(dir, list)

	def __create_model(self, dir, model, iter):
		for item in os.listdir(dir):
			fullname = os.path.join(dir, item)
			if os.path.isdir(fullname):
				child_iter = model.append(iter)
				dirnamefile = os.path.join(fullname, "dirname")
				model.set(child_iter,
					COLUMN_DIR, file(dirnamefile).read().strip(),
					COLUMN_PATH, fullname)

				self.__create_model(fullname, model, child_iter)

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("目录", renderer, text = COLUMN_TITLE)
		self.append_column(column)

class ChooseBook(gtk.VBox):
	"""选择书本的盒子，将DirList和BookList包装起来"""
	def __init__(self, myword):
		gtk.VBox.__init__(self, False, 10)

		self.select_book = None

		hpaned = gtk.HPaned()
		hpaned.show()
		self.pack_start(hpaned)

		self.booklist = BookList()
		self.booklist.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack1(sw)

		dirlist = DirList("books", self.booklist)
		dirlist.show()
		sw.add(dirlist)

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack2(sw)

		sw.add(self.booklist)

		hbox = gtk.HBox(False, 10)
		hbox.show()
		self.pack_end(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_OK)
		button.show()
		button.connect("clicked", self.select_book_cb, myword)
		hbox.pack_end(button, False, False ,0)

		self.show()

	def select_book_cb(self, widget, myword = None):
		model, iter = self.booklist.get_selection().get_selected()

		if iter:
			book = model.get_value(iter, COLUMN_BOOKPATH)

			if ReciteRecord(book).num:
				myword.firstrecite.book = book
				myword.firstrecite.create_model()
				myword.notebook.set_current_page(2)
			else:
				show_info("这本书已经没有需要背诵的单词了.请选择其他书.")
		else:
			show_info("你没有选择任何词典")

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = ChooseBook(win)
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
