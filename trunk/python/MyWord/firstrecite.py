#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import datetime 
import cPickle as pickle
from dictfile import DictFile

class ReciteRecord:
	def __init__(self, path, count = 25):
		self.dict = DictFile(path)
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
	def __init__(self, path):
		gtk.VBox.__init__(self)
		self.path = path

		hpaned = gtk.HPaned()
		self.pack_start(hpaned)

		sw = gtk.ScrolledWindow()
		sw.set_size_request(200, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		textview, self.rr = self.create_textview()
		sw.add(textview)

		hpaned.pack1(sw)

		vbox = gtk.VBox(False, 10)
		button = gtk.Button("确定")
		vbox.pack_end(button, False, False, 0)

		button = gtk.Button("返回")
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

	def create_textview(self):
		textview = gtk.TextView()
		buffer = gtk.TextBuffer()
		
		record = ReciteRecord(self.path)
		buffer.set_text(record.list_word())

		textview.set_buffer(buffer)

		return textview, record

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
        win.add(vbox)

        win.show_all()
	gtk.main()
