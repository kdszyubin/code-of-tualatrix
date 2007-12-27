#!/usr/bin/env python
# coding: utf-8

import gtk
import os
from addword import BookList

class MyWord(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.set_title("MyWord")
		self.set_size_request(400, 200)
		self.connect("destroy", lambda *w: gtk.main_quit())

		vbox = gtk.VBox(False, 0)
		self.add(vbox)

		entry = gtk.Entry()
		entry.connect("activate", self.activate_cb)
		entry.connect("backspace", self.backspace_cb)
		vbox.pack_start(entry)

		self.textview = gtk.TextView()
		buffer = gtk.TextBuffer()
		buffer.set_text("3b'tru:siv")
		self.textview.set_buffer(buffer)
		vbox.pack_end(self.textview, False, False)

		self.show_all()

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
