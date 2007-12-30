#!/usr/bin/env python
# coding: utf-8

import gtk
import gobject
import os

from dictfile import DictFile

(
	COLUMN_TITLE,
	COLUMN_NUM,
	COLUMN_AUTHOR,
) = range(3)

(
	COLUMN_DIR,
	COLUMN_PATH
) = range(2)

class BookList(gtk.TreeView):
	def __init__(self):
		gtk.TreeView.__init__(self)

		model = gtk.ListStore(
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
					COLUMN_TITLE, dict["INFO"]["TITLE"],
					COLUMN_NUM, dict["INFO"]["NUM"],
					COLUMN_AUTHOR, dict["INFO"]["AUTHOR"])

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
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
		mybookdir = os.path.join(os.path.expanduser("~"),".reciteword/books")
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

	def __init__(self):
		gtk.VBox.__init__(self, False, 10)

		hpaned = gtk.HPaned()
		self.pack_start(hpaned)

		listview = BookList()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack1(sw)

		treeview = DirList("/usr/share/reciteword/books", listview)
		sw.add(treeview)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		hpaned.pack2(sw)

		sw.add(listview)

		hbox = gtk.HBox(False, 10)
		self.pack_end(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_GO_BACK)
		hbox.pack_end(button, False, False ,0)

		button = gtk.Button(stock = gtk.STOCK_OK)
		hbox.pack_end(button, False, False ,0)

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = ChooseBook()
        win.add(vbox)

        win.show_all()
	gtk.main()
