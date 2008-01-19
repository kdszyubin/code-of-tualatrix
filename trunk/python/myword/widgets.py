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
import os
import random
import cPickle as pickle

from playsound import read, play

def show_info(message, title = "提示", buttons = gtk.BUTTONS_OK, parent = None):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, buttons)
	dialog.set_icon_from_file("/usr/share/pixmaps/myword.png")
	dialog.set_title(title)
	dialog.set_markup(message)
	dialog.run()
	dialog.destroy()

class MessageDialog(gtk.MessageDialog):

	def __init__(self, 
			message,
			title = "提示",
			parent = None, 
			flags = 0, 
			type = gtk.MESSAGE_INFO,
			buttons = gtk.BUTTONS_YES_NO):
		gtk.MessageDialog.__init__(self, parent, flags, type, buttons)
		self.set_markup(message)
		self.set_title(title)
		self.set_icon_from_file("/usr/share/pixmaps/myword.png")

class WordReview(gtk.VBox):
	def __init__(self, rr, finish_cb):
		gtk.VBox.__init__(self)

		self.rr = rr
		self.finish_cb = finish_cb
		self.passed = False
		self.queue = []

		eventbox = gtk.EventBox()
		eventbox.show()
		eventbox.connect("button_press_event", self.button_press_event)

		self.title = gtk.Label()
		self.title.show()
		eventbox.add(self.title)
		self.pack_start(eventbox, False, False, 20)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.pack_start(hbox, False, False, 0)

		button1 = gtk.Button("Hello")
		button1.show()
		button1.connect("clicked", self.toggled_cb)
		hbox.pack_start(button1, True, True, 5)

		button2 = gtk.Button("Hello")
		button2.show()
		button2.connect("clicked", self.toggled_cb)
		hbox.pack_start(button2, True, True, 5)

		button3 = gtk.Button("Hello")
		button3.show()
		button3.connect("clicked", self.toggled_cb)
		hbox.pack_start(button3, True, True, 5)

		button4 = gtk.Button("Hello")
		button4.show()
		button4.connect("clicked", self.toggled_cb)
		hbox.pack_start(button4, True, True, 5)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.pack_start(hbox, False, False, 10)

		self.status = gtk.Label()
		self.status.show()
		hbox.pack_end(self.status, False, False, 0)

		self.buttons = [button1, button2, button3, button4]

	def start_review(self, rr):
		self.rr = rr
		self.passed = False
		self.queue = []
		self.now = self.rr.words[0]
		self.next()

	def button_press_event(self, widget, event, data = None):
		if self.passed == True:
			self.next()
			self.passed = False

		return False
				
	def remain_list(self):
		remain = self.rr.get_dict().keys()
		remain.remove(self.now)
		return remain

	def toggled_cb(self, widget, data = None):
		cn = widget.get_label()
		lable = self.rr.get_dict()[self.now]
		if cn == lable:
			self.queue.append(self.now)
			play("answerok")
			if len(self.queue) < len(self.rr.words):
				self.status.set_label("回答正确！单击英文标题继续.")
				self.passed = True
			else:
				show_info("回想完毕.请等待下次复习！")
				self.finish_cb(None)
		else:
			play("answerno")
			self.status.set_label("回答错误！请重选.")

	def next(self):
		self.now = self.rr.words[len(self.queue)]
		read(self.now)
		self.title.set_markup('<span size="x-large">%s</span>' % self.now)
		self.status.set_label("第%d个(共%d个)" % (len(self.queue) + 1, len(self.rr.words)))

		answer = random.randint(0, 3)
		self.buttons[answer].set_label(self.rr.get_dict()[self.now])

		filling = random.sample(self.remain_list(), 4)
		for button in self.buttons:
			if self.buttons.index(button) != answer:
				button.set_label(self.rr.get_dict()[filling[self.buttons.index(button)]])

class WordTest(gtk.VBox):
	"""The word test widget for FirstRecite and WordRevise"""
	
	def __init__(self, rr, test_type, return_to, status, update_model, revise = None):
		gtk.VBox.__init__(self)

		self.test_vbox = gtk.VBox(False, 0)
		self.test_vbox.show()
		self.pack_start(self.test_vbox, False, False, 0)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.test_vbox.pack_start(hbox, False, False, 0)

		self.cn = gtk.Label()
		self.cn.show()
		self.cn.set_alignment(0, 0)
		hbox.pack_start(self.cn, False, False, 0)

		button = gtk.Button("发音(_P)", use_underline = True)
		button.connect("clicked", self.speak_button_clicked)
		button.show()
		hbox.pack_end(button, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.show()
		self.entry.connect("activate", self.check_error)
		self.entry.connect("insert-text", self.type_cb)
		self.entry.connect("backspace", self.backspace_cb)
		self.test_vbox.pack_start(self.entry, False, False, 0)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.test_vbox.pack_start(hbox, False, False, 10)

		self.result = gtk.Label()
		self.result.set_alignment(0, 0)
		hbox.pack_start(self.result, False, False, 0)

		self.progress = gtk.Label()
		self.progress.show()
		hbox.pack_end(self.progress, False, False, 0)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.test_vbox.pack_start(hbox)

		button = gtk.Button("不背了！")
		button.show()
		button.connect("clicked", self.exit_test_cb, True)
		hbox.pack_end(button, False, False, 0)

		self.test_type = test_type
		self.return_to = return_to
		self.status = status
		self.update_model = update_model
		self.save_revise = revise

		self.create_test(rr)

		self.review = WordReview(rr, self.exit_test_cb)
		self.pack_start(self.review, False, False, 0)

	def speak_button_clicked(self, widget, data = None):
		read(self.now)

	def create_test(self, rr = None):
		self.rr = rr 
		self.pause = False
		self.correct = False
		self.second = False
		self.passed = []
		self.failed = []
		if self.test_type == "revise":
			self.keep = []
			self.queue = []
		if self.rr:
			self.now = self.next_word()
			self.cn.set_text(self.rr.get_dict()[self.now])
			self.progress.set_text("第1个(共%d)" % self.rr.num)

	def next_word(self):
		return self.rr.words[0]

	def check_error(self, widget, data = None):
		if self.pause == True:
			if self.correct:
				#改错模式
				if len(self.failed) > 0:
					if self.point + 2 > len(self.failed):
						self.progress.set_text("正在改正:剩余%d个" % len(self.failed))
						self.now = self.failed[0]
					else:
						self.progress.set_text("正在改正:剩余%d个" % len(self.failed))
						self.now = self.failed[self.point + 1]
					self.clear_last()
				else:
					if self.test_type == "first":
						if self.second:
							self.finish_test()
						else:
							self.second = True
							self.correct = False
							self.passed = []
							self.failed = []

							self.now = self.next_word()
							self.clear_last()
							show_info("加油！再复习一遍")
							self.progress.set_text("第1个(共%d)" % self.rr.num)
					else:
						self.finish_test()
			else:
				sum = len(self.passed) + len(self.failed)
				if sum != self.rr.num:
					self.progress.set_text("第%d个(共%d)" % (sum + 1, self.rr.num))
				if sum < len(self.rr.words):
					self.now = self.rr.words[sum]
					self.clear_last()
				else:
					if len(self.failed) == 0:
						if self.test_type == "first":
							if self.second:
								self.finish_test()
							else:
								show_info("答完了！再复习一遍")
								self.second = True
								self.correct= False
								self.passed = []
								self.failed = []

								self.now = self.next_word()
								self.clear_last()
						else:
							self.finish_test()
					else:
						self.correct = True
						show_info("现在把答错的改正一下！")
						self.progress.set_text("正在改正:共%d个" % len(self.failed))
						self.now = self.failed[0]
						self.clear_last()
		else:
			self.pause = True
			if self.now == self.entry.get_text():
				self.result.show()
				self.result.set_text("正确!按回车继续.")
				play("answerok")
				if self.now in self.failed:
					self.point = self.failed.index(self.now) - 1
					self.failed.remove(self.now)
				self.passed.append(self.now)
			else:
				self.result.show()
				self.result.set_markup("错误!正确的应该是<b>%s</b>.按回车继续" % self.now)
				play("answerno")
				if not self.now in self.failed:
					self.failed.append(self.now)
				else:
					self.point = self.failed.index(self.now)

	def clear_last(self):
		self.cn.set_text(self.rr.get_dict()[self.now])
		self.result.hide()
		self.result.set_text("")
		self.entry.set_text("")
		self.pause = False

	def save_record(self):
		if self.test_type == "first":
			f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "ab")
			pickle.dump(self.rr, f, True)
			f.close()
		else:
			self.save_revise()

	def finish_test(self):
		self.save_record()
		dialog = MessageDialog("测试完毕！\n还想做次词义回想以加深记忆吗？(可以不做)")
		response = dialog.run()
		if response == gtk.RESPONSE_YES:
			self.status.set_markup('<span size="xx-large">词义回想</span>')
			self.test_vbox.hide()
			self.review.show()
			self.review.start_review(self.rr)
		else:	
			self.exit_test_cb(None)
		dialog.destroy()
		
	def exit_test_cb(self, widget, data = None):
		self.clear_last()
		self.return_to.show()
		if self.test_type == "first":
			self.update_model()
			self.status.set_markup('<span size="xx-large">单词初记-浏览</span>')
		else:
			self.update_model()
			self.status.set_markup('<span size="xx-large">单词复习-浏览</span>')
		self.test_vbox.show()
		self.review.hide()
		self.hide()

	def type_cb(self, widget, new_text, new_text_length, position, data = None):
		if not self.pause:
			play("type")

	def backspace_cb(self, widget, data = None):
		play("back")

if __name__ == "__main__":
	from reciterecord import ReciteRecord
	win = gtk.Window()

	win.connect('destroy', lambda *w: gtk.main_quit())
	win.set_title("Widget Test")
        win.set_default_size(450, 300)
        win.set_border_width(8)

	vbox = WordReview(None, None)
	vbox.start_review(ReciteRecord("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok"))
        vbox.show()
        win.add(vbox)

        win.show()
        gtk.main()
