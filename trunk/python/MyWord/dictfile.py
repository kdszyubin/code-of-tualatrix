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
	separate = ["[C]", "[R]", "[P]"]
	description = ["TITLE", "NUM", "AUTHOR", "OTHER"]

	def __parse(self, filename):
		file = open(filename)
		dictinfo = file.readline()
		dictinfo = dictinfo.split("[N]")[1]
		self["INFO"] = {}
		for sep in self.separate:
			self["INFO"][self.description[self.separate.index(sep)]] = dictinfo.split(sep)[0]
			if self.separate.index(sep) == 3:
				self[self.description[3]] = dictinfo.split(sep)[0]
			else:
				dictinfo = dictinfo.split(sep)[1]
		dictcontent = file.readlines()
		for word in dictcontent:
			if word.find("[M]") != -1:
				word = word.split("[W]")[1]
				if word.find("[T]") != -1:
					self[word.split("[T]")[0]] = word.split("[M]")[1]
				else:
					self[word.split("[M]")[0]] = word.split("[M]")[1]

	def __setitem__(self, key, item):
		if key == "FILE" and item:
			self.__parse(item)
		FileInfo.__setitem__(self, key, item)
