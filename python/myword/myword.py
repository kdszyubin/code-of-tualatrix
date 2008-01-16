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

from revise import Revise
from choosebook import ChooseBook
from firstrecite import FirstRecite
from widgets import show_info
from result import Result
from newword import NewWord

class MyWord(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.config_test()

		self.set_title("Myword 0.7")
		self.set_icon_from_file("/usr/share/pixmaps/myword.png")
		self.set_size_request(500, 300)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("destroy", lambda *w: gtk.main_quit())

		vbox = gtk.VBox(False, 0)
		vbox.show()
		self.add(vbox)

		self.book = gtk.Notebook()
		self.book.show()
		self.book.set_tab_pos(gtk.POS_LEFT)
		vbox.pack_start(self.book)

		welcome = self.welcome()
		welcome.show()
		label = gtk.Label("欢迎")
		self.book.append_page(welcome, label)

		label = gtk.Label("选书")
		self.book.append_page(self.create_choosebook(), label)

		self.firstrecite = self.create_firstrecite()
		self.firstrecite.show()
		label = gtk.Label("初记")
		self.book.append_page(self.firstrecite, label)

		label = gtk.Label("复习")
		self.book.append_page(Revise(), label)

		label = gtk.Label("生词")
		self.book.append_page(NewWord(self), label)

		self.result = Result()
		self.result.show()
		label = gtk.Label("成绩")
		self.book.append_page(self.result, label)

		self.show()

		self.book.set_current_page(0)
		self.book.connect("switch-page", self.switch_page_cb)

	def switch_page_cb(self, widget, page, page_num, data = None):
		if page_num == 4:
			self.result.create_model()

	def config_test(self):
		home_dir = os.path.join(os.path.expanduser("~"), ".myword/books")
		record_file = os.path.join(os.path.expanduser("~"), ".myword/record")
		if not os.path.exists(home_dir):
			os.makedirs(home_dir)

		if not os.path.exists(record_file):
			f = file(record_file, "wb")
			f.close()

	def welcome(self):
		vbox = gtk.VBox(False, 10)

		label = gtk.Label()
		label.show()
		label.set_markup('<span size="xx-large">欢迎使用Myword背单词软件！</span>')
		vbox.pack_start(label)

		return vbox

	def create_choosebook(self):
		vbox = gtk.VBox(False, 10)
		vbox.show()

		book = ChooseBook()
		book.show()
		vbox.pack_start(book)

		hbox = gtk.HBox(False, 10)
		hbox.show()
		vbox.pack_end(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_OK)
		button.show()
		button.connect("clicked", self.select_book_cb, book)
		hbox.pack_end(button, False, False ,0)

		return vbox

	def create_firstrecite(self, book = None):
		return FirstRecite(book)

	def select_book_cb(self, widget, data = None):
		if data.select_book:
			self.firstrecite.book = data.select_book
			self.firstrecite.create_model()
			self.book.set_current_page(2)
		else:
			show_info("你没有选择任何词典")

def main():
	MyWord()
	gtk.main()

if __name__ == "__main__":
	main()
