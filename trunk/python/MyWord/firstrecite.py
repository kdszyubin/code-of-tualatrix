#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import datetime 
import gobject
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
	def __init__(self, book):
		gtk.VBox.__init__(self)
		self.book = book
		self.show()

		# Stage 1, Confirm WordList
		self.wordlist = self.create_wordlist()
		self.pack_start(self.wordlist)

		# Stage 2, Word Preview
		self.preview = self.create_wordpreview()
		self.pack_start(self.preview)
		
	def create_wordlist(self):
		hpaned = gtk.HPaned()
		hpaned.show()

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_size_request(200, -1)
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		listview, self.rr = self.create_listview()
		sw.add(listview)

		hpaned.pack1(sw)

		vbox = gtk.VBox(False, 10)
		vbox.show()

		button = gtk.Button("确定")
		button.show()
		button.connect("clicked", self.button_clicked_cb)
		vbox.pack_end(button, False, False, 0)

		button = gtk.Button("返回")
		button.show()
		vbox.pack_end(button, False, False, 0)

		hpaned.pack2(vbox)

		return hpaned

	def create_wordpreview(self):
		vbox = gtk.VBox(False, 0)

		en = gtk.Label("EN")
		en.show()
		vbox.pack_start(en)
		cn = gtk.Label("CN")
		cn.show()
		vbox.pack_start(cn)

		return vbox

	def button_clicked_cb(self, widget, data = None):
		self.wordlist.hide()
		self.preview.show()

	def create_listview(self):
		listview = gtk.TreeView()
		listview.show()

		model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING)

		record = ReciteRecord(self.book)

		for word in record.words:
			iter = model.append()
			model.set(iter,
				0, word,
				1, record.dict[word].strip())

		listview.set_model(model)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词", renderer, text = 0)
		listview.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("意思", renderer, text = 1)
		listview.append_column(column)

		return listview, record

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(300, 300)
        win.set_border_width(8)

#        vbox = FirstRecite()
        vbox = FirstRecite("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
