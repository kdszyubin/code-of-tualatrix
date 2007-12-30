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

class BookList(gtk.TreeView):
	def __init__(self, dir):
		gtk.TreeView.__init__(self)

		model = gtk.TreeStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING)
		iter = model.append(None)
		model.set(iter, COLUMN_TITLE, "单词库")
		child_iter = model.append(iter)
		model.set(child_iter, COLUMN_TITLE, "我的生词库")
		self.__create_model(os.path.join(os.path.expanduser("~"),".reciteword/books"), model, child_iter)
		self.__create_model(dir, model, iter)

		self.set_model(model)
		self.__add_columns()
		self.expand_all()

	def __create_model(self, dir, model, iter):
		for item in os.listdir(dir):
			fullname = os.path.join(dir, item)
			if os.path.isdir(fullname):
				child_iter = model.append(iter)
				dirnamefile = os.path.join(fullname, "dirname")
				model.set(child_iter, COLUMN_TITLE, file(dirnamefile).read().strip())

				self.__create_model(fullname, model, child_iter)
			elif os.path.basename(fullname) != "dirname":
				child_iter = model.append(iter)
				dict = DictFile(fullname, light = True)
				model.set(child_iter,
					COLUMN_TITLE, dict["INFO"]["TITLE"],
					COLUMN_NUM, dict["INFO"]["NUM"],
					COLUMN_AUTHOR, dict["INFO"]["AUTHOR"])

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Directory", renderer, text = COLUMN_TITLE)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("NUM", renderer, text = COLUMN_NUM)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("AUTHOR", renderer, text = COLUMN_AUTHOR)
		self.append_column(column)

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        win.add(vbox)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create treeview
        treeview = BookList("/usr/share/reciteword/books")
#        treeview.set_rules_hint(True)

        sw.add(treeview)

        win.show_all()
	gtk.main()
