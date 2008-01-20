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

COLUMN_FINISH = COLUMN_TIMES

class Result(gtk.VBox):
	def __init__(self):
		gtk.VBox.__init__(self, False, 10)

		self.rr = None
		self.ing = 0
		self.finished = 0

		label = gtk.Label()
		label.set_markup('<span size="xx-large">你的成绩</span>')
		self.pack_start(label, False, False, 10)

		hpaned = gtk.HPaned()
		hpaned.show()
		self.pack_start(hpaned)

		vbox = gtk.VBox(False, 10)
		hpaned.pack1(vbox)
		self.result_ing = gtk.Label()
		self.result_ing.set_alignment(0, 0)
		vbox.pack_start(self.result_ing, False, False, 10)

		sw = gtk.ScrolledWindow()
		sw.set_size_request(310, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		progress = self.create_progress_list()
		sw.add(progress)

		vbox = gtk.VBox(False, 10)
		hpaned.pack2(vbox)
		self.result_finished = gtk.Label()
		self.result_finished.set_alignment(0, 0)
		vbox.pack_start(self.result_finished, False, False, 10)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		finished = self.create_finished_list()
		sw.add(finished)

	def create_model(self):
		self.create_progress_model()
		self.create_finished_model()

	def create_progress_list(self, finish = None):
		treeview = gtk.TreeView()

		self.progress_model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		treeview.set_model(self.progress_model)
		treeview.set_rules_hint(True)

		self.create_progress_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("组别", renderer, text = COLUMN_GROUP)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("剩余复习次数", renderer, text = COLUMN_TIMES)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("下次复习时间", renderer, text = COLUMN_NEXT)
		treeview.append_column(column)

		return treeview	

	def create_progress_model(self):
		self.progress_model.clear()
		self.ing = 0
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "rb")
		Loading = True

		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				iter = self.progress_model.append()
				self.ing += len(rr.words)
				self.progress_model.set(iter,
					COLUMN_TITLE, rr.get_dict().INFO["TITLE"],
					COLUMN_GROUP, rr.group,
					COLUMN_NUM, len(rr.words),
					COLUMN_TIMES, 7 - rr.time,
					COLUMN_NEXT, rr.next)
		self.result_ing.set_markup("你正在强化记忆<b>%d</b>个单词" % self.ing)
		f.close()

	def create_finished_list(self, finish = None):
		treeview = gtk.TreeView()

		self.finished_model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		treeview.set_model(self.finished_model)
		treeview.set_rules_hint(True)

		self.create_finished_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("组别", renderer, text = COLUMN_GROUP)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		treeview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("完成时间", renderer, text = COLUMN_FINISH)
		column.set_fixed_width(50)
		treeview.append_column(column)

		return treeview	

	def create_finished_model(self):
		self.finished_model.clear()
		self.finished = 0
		f = file(os.path.join(os.path.expanduser("~"), ".myword/finished"), "rb")
		Loading = True

		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				iter = self.finished_model.append()
				self.finished += len(rr.words)
				self.finished_model.set(iter,
					COLUMN_TITLE, rr.get_dict().INFO["TITLE"],
					COLUMN_GROUP, rr.group,
					COLUMN_NUM, len(rr.words),
					COLUMN_FINISH, rr.next)
		self.result_finished.set_markup("你已经掌握了<b>%d</b>个单词" % self.finished)
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
