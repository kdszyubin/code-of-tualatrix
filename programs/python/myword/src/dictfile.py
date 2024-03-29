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
from UserDict import UserDict

class FileInfo(UserDict):
    "store file metadata"
    def __init__(self, filename=None):
        UserDict.__init__(self)
	self.FILE = filename

class DictFile(UserDict):
	"""A book with many words"""
	separate = ["[C]", "[R]", "[P]"]
	description = ["TITLE", "NUM", "AUTHOR", "OTHER"]

	def __init__(self, filename, light = False):
		"""light参数用于决定是否只取得词典的描述"""
		UserDict.__init__(self)

		if os.path.exists(filename):
			self.__parse(filename, light)

	def __parse(self, filename, light):
		"""解析词典，分两步：第一步，获取词典的信息;第二步，获取词典的正文"""
		file = open(filename)
		dictinfo = file.readline()
		dictinfo = dictinfo.split("[N]")[1]
		self.INFO = {"FILE": filename}

		for sep in self.separate:
			self.INFO[self.description[self.separate.index(sep)]] = dictinfo.split(sep)[0]
			if self.separate.index(sep) == 2:
				self.INFO[self.description[3]] = dictinfo.split(sep)[1].strip()
			else:
				dictinfo = dictinfo.split(sep)[1].strip()
		if not light:
			dictcontent = file.readlines()
			for word in dictcontent:
				if word.find("[M]") != -1:
					word = word.split("[W]")[1]
					if word.find("[T]") != -1:
						self[word.split("[T]")[0]] = word.split("[M]")[1].strip()
					else:
						self[word.split("[M]")[0]] = word.split("[M]")[1].strip()
		file.close()

	def __setitem__(self, key, item):
		UserDict.__setitem__(self, key, item)
		self.save()

	def __delitem__(self, key):
		UserDict.__delitem__(self, key)
		self.save()

	def save(self):
		self.INFO["NUM"] = str(len(self.data))
		head = "[H]recitewordbookfile[N]%s[C]%s[R]%s[P]%s\n" % (self.INFO["TITLE"],
									self.INFO["NUM"],
									self.INFO["AUTHOR"],
									self.INFO["OTHER"])
		content = "\n".join(["[W]%s[M]%s" % (k,v) for k,v in self.data.items()])

		f = file(self.INFO["FILE"], "wb")
		f.write(head + content)
		f.close()

	def __str__(self):
		return self.INFO["FILE"]

	def to_string(self):
		return "".join(["%s\t%s" % (k, v) for k, v in self.data.items()])

class SentenceFile(UserDict):
	"""SentenceFile用于使用保存例句的文件"""
	def __init__(self):
		UserDict.__init__(self)

		self.__parse()

	def __parse(self):
		for sentence in file(os.path.join(os.path.expanduser("~"), ".myword/sentence")):
			self[sentence.split(":")[0]] = sentence.split(":")[1].strip()

	def __setitem__(self, key, item):
		UserDict.__setitem__(self, key, item)
		self.save()

	def __delitem__(self, key):
		UserDict.__delitem__(self, key)
		self.save()

	def save(self):
		content = "\n".join(["%s:%s" % (k,v) for k,v in self.data.items()])

		f = file(os.path.join(os.path.expanduser("~"), ".myword/sentence"), "wb")
		f.write(content)
		f.close()
