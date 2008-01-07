#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import datetime
import gobject
import cPickle as pickle

from dictfile import DictFile
from reciterecord import ReciteRecord
from playsound import read, play
from widgets import show_info
from widgets import WordTest

(
	COLUMN_ID,
	COLUMN_TITLE,
	COLUMN_GROUP,
	COLUMN_NUM,
	COLUMN_TIMES,
) = range(5)

class Revise(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self)
		self.show()

		self.rr = None
		self.queue = []
		self.keep = []

		self.status = gtk.Label()
		self.status.show()
		self.status.set_markup('<span size="xx-large">单词复习-浏览</span>')
		self.pack_start(self.status, False, False, 10)

		# Stage 1, Confirm WordList
		self.reviselist = self.create_reviselist()
		self.pack_start(self.reviselist, True, True, 10)

		# Stage 2, test function
		self.wordtest = WordTest(self.rr,
					"revise",
					self.reviselist,
					self.status,
					self.update_record)
		self.pack_start(self.wordtest, False, False, 10)

	def update_record(self):
		self.rr.next = self.rr.nextime()
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "wb")
		self.queue.extend(self.keep)
		for rr in self.queue:
			pickle.dump(rr, f, True)
			
		f.close()
		self.reviselist.show()
		self.wordtest.hide()

		self.create_model()
		
	def create_reviselist(self):
		hpaned = gtk.HPaned()
		hpaned.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_size_request(400, -1)
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

		button = gtk.Button("确定")
		button.show()
		button.connect("clicked", self.start_revise_cb)
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

		return hpaned

	def start_revise_cb(self, widget, data = None):
		self.wordtest.create_test(self.rr)
		self.reviselist.hide()
		self.status.set_markup('<span size="xx-large">单词复习-测试</span>')
		self.wordtest.entry.grab_focus()
		self.wordtest.show()

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
		column = gtk.TreeViewColumn("ID", renderer, text = COLUMN_ID)
		listview.append_column(column)


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
		column = gtk.TreeViewColumn("第几次复习", renderer, text = COLUMN_TIMES)
		listview.append_column(column)

		selection = listview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed)

		return listview

	def create_model(self):
		self.model.clear()
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
				if datetime.date.today() >= rr.next:
					iter = self.model.append()
					self.queue.append(rr)
					self.model.set(iter,
						COLUMN_ID, len(self.queue) - 1,
						COLUMN_TITLE, rr.dict.INFO["TITLE"],
						COLUMN_GROUP, rr.group,
						COLUMN_NUM, len(rr.words),
						COLUMN_TIMES, rr.time)
				else:
					self.keep.append(rr)

		f.close()

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			self.rr = self.queue[int(model.get_value(iter, COLUMN_ID))]
			self.wordtest.now = self.rr.words[0]
			self.wordtest.cn.set_text(self.rr.dict[self.wordtest.now])
			self.wordtest.progress.set_text("第1个(共%d)" % self.rr.num)

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

	vbox = Revise()
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()