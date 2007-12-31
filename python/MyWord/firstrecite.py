#!/usr/bin/env python
# coding: utf-8

import gtk
import datetime 
from dictfile import DictFile

class ReciteRecord:
	def __init__(self, path, count = 25):
		self.dict = DictFile(path)
		self.INTERVAL = (0, 1, 1, 2, 3, 7)
		self.words = []
		self.num = count
		self.time = 1
		self.next = self.nextime(True)
		for k in self.dict.keys():
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

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.pack_start(sw)

		textview = self.create_textview(path)
		sw.add(textview)

	def create_textview(self, path):
		textview = gtk.TextView()
		buffer = gtk.TextBuffer()
		
		record = ReciteRecord(path)
		buffer.set_text(record.list_word())

		textview.set_buffer(buffer)

		return textview

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(400, 300)
        win.set_border_width(8)

        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
        win.add(vbox)

        win.show_all()
	gtk.main()
