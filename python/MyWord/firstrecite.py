#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import datetime 
import time
import cPickle as pickle
from dictfile import DictFile

class ReciteRecord:
	def __init__(self, book, count = 25):
		self.dict = DictFile(book)
		self.INTERVAL = (0, 1, 1, 2, 3, 7)
		self.words = []
		self.exclude = []
		self.num = count
		self.time = 1
		self.next = self.nextime(True)

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
				if rr.dict.INFO["TITLE"] == self.dict.INFO["TITLE"]:
					self.exclude.extend(rr.words)
		f.close()

		for k in self.dict.keys():
			if k in self.exclude:
				pass
			else:
				self.words.append(k)
				count -= 1
				if count == 0:
					break
			
	def nextime(self, first = None):
		today = datetime.date.today()
		if first:
			next = today + datetime.timedelta(1)
		else:	
			next = today + datetime.timedelta(self.INTERVAL[self.time])
			self.time += 1

		return next

	def list_word(self):
		 return "".join(["%s\t%s" % (word, self.dict[word]) for word in self.words])

class FirstRecite(gtk.VBox):
	def __init__(self, book = None):
		gtk.VBox.__init__(self)
		if book:
			self.book = book
			self.create_words_list()

	def create_words_list(self):
		self.hpaned = gtk.HPaned()
		self.pack_start(self.hpaned)

		sw = gtk.ScrolledWindow()
		sw.set_size_request(200, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		textview, self.rr = self.create_textview()
		sw.add(textview)

		self.hpaned.pack1(sw)

		vbox = gtk.VBox(False, 10)
		button = gtk.Button("确定")
		button.connect("clicked", self.button_clicked_cb)
		vbox.pack_end(button, False, False, 0)

		button = gtk.Button("返回")
		vbox.pack_end(button, False, False, 0)

		self.hpaned.pack2(vbox)

	def button_clicked_cb(self, widget, data = None):
		self.hpaned.destroy()
		self.create_wordpreview()

	def create_wordpreview(self):
		en = gtk.Label("")
		self.pack_start(en)
		cn = gtk.Label("")
		self.pack_start(cn)
		for word in self.rr.words:
			en.set_text(word)
			cn.set_text(self.rr.dict[word])

	def create_textview(self):
		textview = gtk.TextView()
		buffer = gtk.TextBuffer()
		
		record = ReciteRecord(self.book)
		buffer.set_text(record.list_word())

		textview.set_buffer(buffer)

		return textview, record

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

#        vbox = FirstRecite()
        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
        win.add(vbox)

        win.show_all()
	gtk.main()
