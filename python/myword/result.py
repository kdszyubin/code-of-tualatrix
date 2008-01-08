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
import cPickle as pickle

from dictfile import DictFile

(
	COLUMN_TITLE,
	COLUMN_GROUP,
	COLUMN_NUM,
	COLUMN_TIMES,
	COLUMN_NEXT,
) = range(5)

(
	COLUMN_START,
	COLUMN_FINISH,
) = range(3,5)

class Result(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 10)
		self.rr = None

		self.ing = 0
		self.finished = 0

		label = gtk.Label()
		label.show()
		label.set_markup('<span size="xx-large">你的成绩</span>')
		self.pack_start(label, False, False, 10)

		self.result_ing = gtk.Label()
		self.result_ing.set_alignment(0, 0)
		self.result_ing.show()
		self.pack_start(self.result_ing, False, False, 10)

		listview = self.create_listview()
		listview.show()
		self.pack_start(listview)

	def create_listview(self, finish = None):
		listview = gtk.TreeView()

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
		self.model.clear()
		self.ing = 0
		self.finished = 0
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
		self.result_ing.set_markup("你正在强化记忆<b>%d</b>个单词" % self.ing)
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
