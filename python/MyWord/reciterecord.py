#!/usr/bin/env python
# coding: utf-8

import os
import datetime
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

if __name__ == "__main__":
	rr = ReciteRecord("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
	print "The dict is %s." % rr.dict.INFO["TITLE"]
	print "words to recite %s." % rr.words
	print "You have revised for %d time(s)." % rr.time
	print "Next time to revise is %s" % rr.next
