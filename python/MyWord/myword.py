#!/usr/bin/env python
# coding: utf-8

import gtk
import os
from choosebook import ChooseBook
from firstrecite import FirstRecite
from widgets import show_info
from result import Result

class MyWord(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.set_title("TXRecite")
		self.set_size_request(600, 400)
		self.connect("destroy", lambda *w: gtk.main_quit())

		vbox = gtk.VBox(False, 0)
		self.add(vbox)

		self.book = gtk.Notebook()
		self.book.set_tab_pos(gtk.POS_LEFT)
		vbox.pack_start(self.book)

		welcome = self.welcome()
		label = gtk.Label("欢迎")
		self.book.append_page(welcome, label)

		#page 选书
		label = gtk.Label("选书")
		self.book.append_page(self.create_choosebook(), label)

		#初记
		self.firstrecite = self.create_firstrecite()
		label = gtk.Label("初记")
		self.book.append_page(self.firstrecite, label)

		button = gtk.Button("Welcome")
		label = gtk.Label("复习")
		self.book.append_page(button, label)

		self.result = Result()
		label = gtk.Label("成绩")
		self.book.append_page(self.result, label)

		self.show_all()

		self.book.set_current_page(0)

	def welcome(self):
		vbox = gtk.VBox(False, 10)

		label = gtk.Label()
		label.set_markup("Hello！欢迎使用Myword背单词软件！")
		vbox.pack_start(label)

		return vbox

	def create_choosebook(self):
		vbox = gtk.VBox(False, 10)

		book = ChooseBook()
		vbox.pack_start(book)

		hbox = gtk.HBox(False, 10)
		vbox.pack_end(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_GO_BACK)
		hbox.pack_end(button, False, False ,0)

		button = gtk.Button(stock = gtk.STOCK_OK)
		button.connect("clicked", self.select_book_cb, book)
		hbox.pack_end(button, False, False ,0)

		return vbox

	def create_firstrecite(self, book = None):
		return FirstRecite(book)

	def select_book_cb(self, widget, data = None):
		if data.select_book:
			print data.select_book
			self.firstrecite.book = data.select_book
			self.firstrecite.create_model()
		else:
			show_info("你没有选择任何词典")

	def activate_cb(self, widget, data = None):
		books = BookList("/usr/share/reciteword/books") 
		added = False
		for book in books:
			for word in file(book):
				if word.find("[W]" + widget.get_text() + "[T]") >= 0:
					tualatrix = open(os.path.join(os.path.expanduser("~"),".reciteword/books/txwords-5.bok"), "a")
					tualatrix.write(word)
					tualatrix.close()
					buffer = gtk.TextBuffer()
					buffer.set_text("正在搜寻第%d本...找到'%s: %s'并已加入生词本" % ((books.index(book) + 1), widget.get_text(), word.split('[W]')[1].split('[T]')[1].split('[M]')[1].strip()))
					self.textview.set_buffer(buffer)
					added = True
					break
			if added:
				break
			else:
				buffer = gtk.TextBuffer()
				buffer.set_text("正在搜寻第%d本...找不到！" % (books.index(book) + 1))
				self.textview.set_buffer(buffer)

	def backspace_cb(self, widget, data = None):
		print widget.set_text("")
def main():
	MyWord()
	gtk.main()

if __name__ == "__main__":
	main()
