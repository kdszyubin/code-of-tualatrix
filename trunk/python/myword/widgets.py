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
import cPickle as pickle

from playsound import read, play

def show_info(message, title = "提示", parent = None):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
	dialog.set_title(title)
	dialog.set_markup(message)
	dialog.run()
	dialog.destroy()

class WordTest(gtk.VBox):
	"""The word test widget for FirstRecite and WordRevise"""
	
	def __init__(self, rr, test_type, return_to, status, update_model):
		gtk.VBox.__init__(self)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.pack_start(hbox, False, False, 0)

		self.cn = gtk.Label()
		self.cn.show()
		self.cn.set_alignment(0, 0)
		hbox.pack_start(self.cn, False, False, 0)

		button = gtk.Button("读一下!")
		button.connect("clicked", self.speak_button_clicked)
		button.show()
		hbox.pack_end(button, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.show()
		self.entry.connect("activate", self.check_error)
		self.entry.connect("insert-text", self.type_cb)
		self.entry.connect("backspace", self.backspace_cb)
		self.pack_start(self.entry, False, False, 0)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.pack_start(hbox, False, False, 10)

		self.result = gtk.Label()
		self.result.set_alignment(0, 0)
		hbox.pack_start(self.result, False, False, 0)

		self.progress = gtk.Label()
		self.progress.show()
		hbox.pack_end(self.progress, False, False, 0)

		hbox = gtk.HBox(False, 0)
		hbox.show()
		self.pack_start(hbox)

		button = gtk.Button("不背了！")
		button.show()
		button.connect("clicked", self.finish_test_cb, True)
		hbox.pack_end(button, False, False, 0)

		self.test_type = test_type
		self.return_to = return_to
		self.status = status
		self.update_model = update_model

		self.create_test(rr)

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
			self.now = self.rr.words[0]
			self.cn.set_text(self.rr.dict[self.now])
			self.progress.set_text("第1个(共%d)" % self.rr.num)

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
							show_info("本次测试结束了！下次再提醒你复习！")
							self.save_record()
							self.finish_test_cb(None)
						else:
							self.second = True
							self.correct = False
							self.passed = []
							self.failed = []

							self.now = self.rr.words[0]
							self.clear_last()
							show_info("加油！再复习一遍")
							self.progress.set_text("第1个(共%d)" % self.rr.num)
					else:
						show_info("好了！等我提醒你复习吧！")
						self.save_record()
						self.finish_test_cb(None)
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
								show_info("好了！等我提醒你复习吧！")
								self.save_record()
								self.finish_test_cb(None)
							else:
								show_info("答完了！再复习一遍")
								self.second = True
								self.correct= False
								self.passed = []
								self.failed = []

								self.now = self.rr.words[0]
								self.clear_last()
						else:
							show_info("好了！等我提醒你复习吧！")
							self.save_record()
							self.finish_test_cb(None)
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
		self.cn.set_text(self.rr.dict[self.now])
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
			self.update_model()
		
	def finish_test_cb(self, widget, data = None):
		self.clear_last()
		self.return_to.show()
		if self.test_type == "first":
			self.update_model()
			self.status.set_markup('<span size="xx-large">单词初记-浏览</span>')
		else:
			self.status.set_markup('<span size="xx-large">单词复习-浏览</span>')
		self.hide()

	def type_cb(self, widget, new_text, new_text_length, position, data = None):
		if not self.pause:
			play("type")

	def backspace_cb(self, widget, data = None):
		play("back")
