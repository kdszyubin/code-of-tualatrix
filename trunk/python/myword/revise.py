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

		#rr属性即ReciteRecord
		self.rr = None
		#model属性是当前单词的列表，动态更新
		self.model = None
		#pause属性来判断单词测试时，是输入状态还是确认状态
		self.pause = False
		#correct属性用来决定当前是否是改正模式
		self.correct = False
		#keep列表用于保存读入的背诵纪录中不需要复习的
		self.keep = []
		#queue列表用于保存正要复习的记录
		self.queue = []
		#passed列表中存储测试中通过的单词
		self.passed = []
		#failed列表中存储测试中做错的单词，供第二次改正时使用
		self.failed = []

		# Stage 1, Confirm WordList
		self.preview = self.create_reviselist()
		self.pack_start(self.preview)

		# Stage 2, test function
		self.wordtest = self.create_test()
		self.pack_start(self.wordtest)

	def update_record(self):
		self.rr.next = self.rr.nextime()
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "wb")
		if self.keep:
			for rr in self.keep:
				pickle.dump(self.rr, f, True)

		if self.queue:
			for rr in self.queue:
				pickle.dump(self.rr, f, True)
			
		f.close()
		self.preview.show()
		self.wordtest.hide()
		
	def create_reviselist(self):
		hpaned = gtk.HPaned()
		hpaned.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_size_request(200, -1)
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
		button.connect("clicked", self.button_clicked_cb)
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

		return hpaned

	def create_test(self):
		vbox = gtk.VBox(False, 0)

		self.cn = gtk.Label()
		if self.rr:
			self.now = self.rr.words[0]
			self.cn.set_text(self.rr.dict[self.now])
		self.cn.set_alignment(0, 0)
		self.cn.show()
		vbox.pack_start(self.cn, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.connect("activate", self.check_cb)
		self.entry.connect("insert-text", self.type_cb)
		self.entry.connect("backspace", self.backspace_cb)
		self.entry.show()
		vbox.pack_start(self.entry, False, False, 0)

		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, False, False, 0)

		self.result = gtk.Label()
		self.result.set_alignment(0, 0)
		hbox.pack_start(self.result, False, False, 0)

		self.progress = gtk.Label()
		self.result.set_alignment(1,0)
		hbox.pack_end(self.progress, False, False, 0)

		return vbox

	def check_cb(self, widget, data = None):
		if self.pause == True:
			if self.correct:
				sum = len(self.failed)
				self.progress.set_text("正在改正，还有%d题" % sum)
				if len(self.failed) > 0:
					self.now = self.failed[len(self.failed) - 1]
					self.cn.set_text(self.rr.dict[self.now])
					self.result.hide()
					self.result.set_text("")
					self.entry.set_text("")
					self.pause = False
				else:
					show_info("下次再提醒你复习！")
					self.update_record()
			else:
				sum = len(self.passed) + len(self.failed)
				self.progress.set_text("第%d个(共%d)" % (sum, self.rr.num))
				if sum < len(self.rr.words):
					self.now = self.rr.words[sum]
					self.cn.set_text(self.rr.dict[self.now])
					self.result.hide()
					self.result.set_text("")
					self.entry.set_text("")
					self.pause = False
				else:
					if len(self.failed) == 0:
						show_info("好了！等我提醒你复习吧！")
						self.update_record()
					else:
						self.correct = True
						show_info("你错了好几个啊！现在改正一下！")
						self.now = self.failed[len(self.failed) - 1]
						self.cn.set_text(self.rr.dict[self.now])
						self.result.hide()
						self.result.set_text("")
						self.entry.set_text("")
						self.pause = False
		else:
			self.pause = True
			if self.now == self.entry.get_text():
				self.result.show()
				self.result.set_text("正确.按任意键继续.")
				play("answerok")
				if self.now in self.failed:
					self.failed.remove(self.now)
				self.passed.append(self.now)
			else:
				self.result.show()
				self.result.set_text("错误.正确的应该是%s.按任意键继续" % self.now)
				play("answerno")
				if not self.now in self.failed:
					self.failed.append(self.now)

	def type_cb(self, widget, new_text, new_text_length, position, data = None):
		if not self.pause:
			play("type")

	def backspace_cb(self, widget, data = None):
		play("back")

	def button_clicked_cb(self, widget, data = None):
		self.preview.hide()
		self.entry.grab_focus()
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
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "rb")
		Loading = True

		while Loading:
			try:
				rr = pickle.load(f)
				print rr
			except pickle.UnpicklingError:
				print "截入错误，应该是空记录"
			except EOFError:
				Loading = False
				print "载入完毕"
			else:
				iter = self.model.append()
				if datetime.date.today() >= rr.next:
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
			self.now = self.rr.words[0]
			self.cn.set_text(self.rr.dict[self.now])

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

	vbox = Revise()
	vbox.show()
        win.add(vbox)

        win.show_all()
	gtk.main()
