#!/usr/bin/env python
# coding: utf-8

import sys
import os
import glob
from UserList import UserList


class BookList(UserList):
        def __init__(self, path):
                UserList.__init__(self)
                self.createbookdir(path)

        def createbookdir(self, path):
                for file in os.listdir(path):
                        hasbooks = glob.glob(path + "/" + file + "/*.bok")
                        if not hasbooks:
                                file = path + "/" + file
                                if os.path.isdir(file):
                                        self.createbookdir(file)
                        else:
                                self.extend(hasbooks)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "command error!"
		sys.exit(1)
	books = BookList("/usr/share/reciteword/books") 
	for book in books:
		for word in file(book):
			if word.find("[W]"+sys.argv[1]+"[T]") >= 0:
				tualatrix = open("/home/tualatrix/.reciteword/books/txwords-2.bok", "a")
				tualatrix.write(word)
				tualatrix.close()
				print "找到了！把'" + word + "'加到你的生词库里了！"
				sys.exit(0)
		print "找完了第%d本，找不到！" % books.index(book)
