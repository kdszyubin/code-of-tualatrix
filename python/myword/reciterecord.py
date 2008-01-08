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

import os
import datetime
import cPickle as pickle
from dictfile import DictFile

class ReciteRecord:
	def __init__(self, book, count = 25):
		self.dict = DictFile(book)
		self.INTERVAL = (0, 1, 1, 2, 3, 7, 14)
		self.words = []
		self.exclude = []
		self.num = count
		self.time = 1
		self.next = self.nextime(True)
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

		self.cleanup()

	def cleanup(self):
		for word in self.dict.keys():
			if not word in self.words:
				del self.dict[word]
			
	def nextime(self, first = None):
		today = datetime.date.today()
		if first:
			next = today + datetime.timedelta(1)
		else:	
			next = today + datetime.timedelta(self.INTERVAL[self.time + 1])
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
