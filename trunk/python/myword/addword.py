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
				tualatrix = open(os.path.join(os.path.expanduser("~"),".myword/books/txwords-1.bok"), "a")
				tualatrix.write(word)
				tualatrix.close()
				print "正在搜寻第%d本...找到'%s: %s'并已加入生词本" % ((books.index(book) + 1), sys.argv[1], word.split('[W]')[1].split('[T]')[1].split('[M]')[1].strip())
				sys.exit(0)
		print "找完了第%d本，找不到！" % (books.index(book) + 1)
