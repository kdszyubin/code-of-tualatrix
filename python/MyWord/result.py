#!/usr/bin/env python
# coding: utf-8

import gtk
import gobject
import os
import cPickle as pickle

from dictfile import DictFile

(
	COLUMN_TITLE,
	COLUMN_GROUP,
	COLUMN_NUM,
	COLUMN_TIMES,
	COLUMN_NEXT,
) = range(5)

class Result(gtk.VBox):

	def __init__(self):
		gtk.VBox.__init__(self, False, 10)
		self.rr = None

		self.ing = 0
		self.finished = 0

		self.result = gtk.Label()
		self.pack_start(self.result)

		listview = self.create_listview()

		self.pack_start(listview)

	def create_listview(self):
		listview = gtk.TreeView()

		listview.show()

		self.model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		listview.set_model(self.model)

		self.create_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("组别", renderer, text = COLUMN_GROUP)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("剩余复习次数", renderer, text = COLUMN_TIMES)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("下次复习时间", renderer, text = COLUMN_NEXT)
		listview.append_column(column)

		return listview	

	def create_model(self):
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "rb")
		Loading = True

		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				print "截入错误，应该是空记录"
			except EOFError:
				Loading = False
				print "载入完毕"
			else:
				iter = self.model.append()
				if rr.time < 7:
					self.ing += len(rr.words)
				else:
					self.finished += len(rr.words)
				self.model.set(iter,
					COLUMN_TITLE, rr.dict.INFO["TITLE"],
					COLUMN_GROUP, rr.group,
					COLUMN_NUM, len(rr.words),
					COLUMN_TIMES, 7 - rr.time,
					COLUMN_NEXT, rr.next)
		self.result.set_markup("你一共背了<b>%d</b>个单词，强化复习了<b>%d</b>个单词" % (self.ing, self.finished))
		f.close()

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
