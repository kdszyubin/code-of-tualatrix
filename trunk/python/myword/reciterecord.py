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
	"""背诵纪录的类，记录着当前背诵的书本的文件名(dict)，单词列表(words)
	和排除列表(exclude)，排除列表是为避免同一本书取到相同的单词，因为单
	词都是随机选的，time代表下次复习为第几次
	会保存"""
	interval = (0, 1, 1, 2, 4, 7, 14)

	def __init__(self, filename, count = 25):
		self.dict = filename
		self.words = []
		self.exclude = []
		self.num = 0
		self.time = 1
		self.next = self.set_next(True)
		self.group = 1

		self.create_wordlist(count)

	def create_wordlist(self, count = None):
		"""创建单词列表，返回单词数"""
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "rb")
		
		Loading = True
		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				if rr.get_dict().INFO["TITLE"] == self.get_dict().INFO["TITLE"]:
					self.exclude.extend(rr.words)
					self.group += 1
		f.close()

		f = file(os.path.join(os.path.expanduser("~"), ".myword/finished"), "rb")
		
		Loading = True
		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				if rr.get_dict().INFO["TITLE"] == self.get_dict().INFO["TITLE"]:
					self.exclude.extend(rr.words)
					self.group += 1
		f.close()

		for k in self.get_dict().keys():
			if k in self.exclude:
				pass
			else:
				self.words.append(k)
				count -= 1
				if count == 0:
					break

		self.num = len(self.words)

		return self.num

	def get_dict(self):
		"""根据纪录信息打开词典并返回"""
		return DictFile(self.dict)
			
	def set_next(self, first = None):
		"""根据interval时间间隔列表和当前的次数(time)，自动设置下
		次复习时间。first参数只用于第一次产生复习时间"""
		today = datetime.date.today()

		if first:
			next = today + datetime.timedelta(1)
		else:	
			next = today + datetime.timedelta(self.interval[self.time + 1])
			self.time += 1

		return next

	def list_word(self):
		"""返回当前纪录的单词列表"""
		return "".join(["%s\t%s" % (word, self.get_dict()[word]) for word in self.words])  

	def finish_recite(self):
		"""当第六次复习完毕，就触发这个方法，以完成一个纪录"""
		f = file(os.path.join(os.path.expanduser("~"), ".myword/finished"), "ab")
		pickle.dump(self, f, True)
		f.close()

if __name__ == "__main__":
	rr = ReciteRecord("/usr/share/reciteword/books/qqssbdc/cykych/ck-kq.bok")
	print "要背诵的书是:%s." % rr.get_dict().INFO["TITLE"]
	print "需要背育的单词是:%s." % rr.words
	print "还需要复习%d次才算掌握." % (7 - rr.time)
	print "下次复习的时间是:%s" % rr.next
