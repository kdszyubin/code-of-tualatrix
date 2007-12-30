#!/usr/bin/env python
# coding: utf-8

from UserDict import UserDict

class FileInfo(UserDict):
    "store file metadata"
    def __init__(self, filename=None):
        UserDict.__init__(self)
	self["FILE"] = filename

class DictFile(FileInfo):
	"""A book with many words"""
	separate = ["[C]", "[R]", "[P]", "[A]"]
	description = ["TITLE", "NUM", "AUTHOR", "OTHER"]

	#继承自FileInfo，light参数用于决定是否只取得词典的描述
	def __init__(self, filename, light = False):
		FileInfo.__init__(self, filename)
		self.__parse(filename, light)

	#解析词典，分两步：第一步，获取词典的信息;第二步，获取词典的正文
	def __parse(self, filename, light):
		file = open(filename)
		dictinfo = file.readline()
		dictinfo = dictinfo.split("[N]")[1]
		self["INFO"] = {}

		for sep in self.separate:
			self["INFO"][self.description[self.separate.index(sep)]] = dictinfo.split(sep)[0]
			if self.separate.index(sep) == 2:
				self[self.description[3]] = dictinfo.split(sep)[1]
			else:
				dictinfo = dictinfo.split(sep)[1]
		if not light:
			dictcontent = file.readlines()
			for word in dictcontent:
				if word.find("[M]") != -1:
					word = word.split("[W]")[1]
					if word.find("[T]") != -1:
						self[word.split("[T]")[0]] = word.split("[M]")[1]
					else:
						self[word.split("[M]")[0]] = word.split("[M]")[1]
		file.close()
