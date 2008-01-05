#!/usr/bin/env python
# coding: utf-8

import os
import datetime
import cPickle as pickle
from dictfile import DictFile

class ReciteRecord:
	def __init__(self, book, count = 25):
		#dict，书名
		self.dict = DictFile(book)
		#6次复习间隔
		self.INTERVAL = (0, 1, 1, 2, 3, 7, 14)
		#背诵单词列表
		self.words = []
		#exclude用于如果是同一本书，则选不包括的单词
		self.exclude = []
		#count即单词数，用于产生words的数目
		self.num = count
		#7-time表示还需要几次复习
		self.time = 1
		#next下次背诵时间
		self.next = self.nextime(True)
		#group书的第几组
		self.group = 1

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
					self.group += 1
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
	print "要背诵的书是:%s." % rr.dict.INFO["TITLE"]
	print "需要背育的单词是:%s." % rr.words
	print "还需要复习%d次才算掌握." % (7 - rr.time)
	print "下次复习的时间是:%s" % rr.next
