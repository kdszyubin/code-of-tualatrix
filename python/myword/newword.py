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

import gtk
import gobject
import sys
import os
import glob
import datetime

from widgets import MessageDialog
from dictfile import DictFile
from playsound import read
from UserList import UserList

(
	COLUMN_TITLE,
	COLUMN_NUM,
	COLUMN_PATH,
	COLUMN_EDITABLE_OF_BOOK,
) = range(4)

(
	COLUMN_EN,
	COLUMN_CN,
	COLUMN_EDITABLE,
) = range(3)

class ExistBook(UserList):
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

class BookList(gtk.TreeView):
	"""the new word book list"""
	def __init__(self, list = None):
		gtk.TreeView.__init__(self)

		model = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_STRING,
			gobject.TYPE_BOOLEAN)

		self.set_model(model)
		self.update_list(model)

		self.__add_columns()
		self.set_rules_hint(True)
		self.set_size_request(180, -1)
		self.expand_all()

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed, list)

	def selection_changed(self, widget, list):
		model, iter = widget.get_selected()
		if iter:
			book = model.get_value(iter, COLUMN_PATH)
			if book:
				list.update_list(book)

	def update_list(self, model):
		model.clear()
		booksdir = os.path.join(os.path.expanduser("~"), ".myword/books")
		for item in os.listdir(booksdir):
			fullname = os.path.join(booksdir, item)
			dict = DictFile(fullname, light = True)
			iter = model.append()
			model.set(iter,
				COLUMN_TITLE, dict.INFO["TITLE"],
				COLUMN_NUM, dict.INFO["NUM"],
				COLUMN_PATH, fullname,
				COLUMN_EDITABLE_OF_BOOK, True)

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		renderer.connect("edited", self.on_cell_edited, model)
		column = gtk.TreeViewColumn("书名", renderer, text = COLUMN_TITLE, editable = COLUMN_EDITABLE_OF_BOOK)
		column.set_sort_column_id(COLUMN_TITLE)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("单词数", renderer, text = COLUMN_NUM)
		column.set_sort_column_id(COLUMN_NUM)
		self.append_column(column)

	def on_cell_edited(self, cell, path_string, new_text, model):
		iter = model.get_iter_from_string(path_string)
		book = DictFile(model.get_value(iter, COLUMN_PATH))
		book.INFO['TITLE'] = new_text
		book.save()
		model.set_value(iter, COLUMN_TITLE, new_text)

class WordList(gtk.TreeView):
	"""Show a full list of a book"""
	def __init__(self, parent):
		gtk.TreeView.__init__(self)

		model = gtk.ListStore(
				gobject.TYPE_STRING,
				gobject.TYPE_STRING,
				gobject.TYPE_BOOLEAN)

		self.set_model(model)
		self.set_rules_hint(True)

		renderer = gtk.CellRendererText()
		renderer.connect("edited", self.on_cell_edited, model)
		renderer.set_data("column", COLUMN_EN)
		column = gtk.TreeViewColumn("单词", renderer, text = COLUMN_EN, editable = COLUMN_EDITABLE)
		column.set_sort_column_id(COLUMN_EN)
		self.append_column(column)

		renderer = gtk.CellRendererText()
		renderer.connect("edited", self.on_cell_edited, model)
		renderer.set_data("column", COLUMN_CN)
		column = gtk.TreeViewColumn("中文解释", renderer, text = COLUMN_CN, editable = COLUMN_EDITABLE)
		self.append_column(column)

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_BROWSE)
		selection.connect("changed", self.selection_changed)

		menu = self.create_popup_menu(parent)
		menu.show_all()
		self.connect("button_press_event", self.button_press_event, menu)

	def on_cell_edited(self, cell, path_string, new_text, model):
		"""在编辑完单元格后触发，这个回调函数提供了很多有用的值：
		cell是编辑的单元格，即一个GtkCellRendererText；
		path_string是这个单元格所处位置的下标，String类型；
		new_text是编辑后的文本。
		下面三句代码分别是：取得当前位置的iter，取得当前单元格的分类，设置新的分类"""
		iter = model.get_iter_from_string(path_string)
		column = cell.get_data("column")

		model.set_value(iter, column, new_text)

		self.save(model)

	def save(self, model):
		"""将更新后的列表内容保存"""
		book = DictFile(self.book)
		book.clear()

		iter = model.get_iter_first()
		while iter:
			book[model.get_value(iter, COLUMN_EN)] = model.get_value(iter, COLUMN_CN)
			iter = model.iter_next(iter)
		book.save()

		booklist = self.get_data("booklist")
		model = booklist.get_model()
		booklist.update_list(model)

	def create_popup_menu(self, parent):
		menu = gtk.Menu()
		group = gtk.AccelGroup()

		parent.add_accel_group(group)
		menu.set_accel_group(group)

		new = gtk.MenuItem("新增")
		new.connect("activate", self.add_new_word)
		remove = gtk.MenuItem("删除")
		remove.connect("activate", self.remove_selected_word)
		
		menu.append(new)
		menu.append(remove)
		menu.attach_to_widget(self, None)

		return menu

	def add_new_word(self, widget, data = None):
		model = self.get_model()
		iter = model.append()
		model.set(iter,
			COLUMN_EN, "在此输入英文",
			COLUMN_CN, "在此输入中文",
			COLUMN_EDITABLE, True)

	def remove_selected_word(self, widget, data = None):
		model, iter = self.get_selection().get_selected()
		model.remove(iter)

		self.save(model)

		booklist = self.get_data("booklist")
		model = booklist.get_model()
		booklist.update_list(model)

	def button_press_event(self, widget, event, data = None):
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
			data.popup(None, None, None, event.button, event.time)
		return False

	def update_list(self, book):
		self.book = book
		model = self.get_model()
		model.clear()
		self.dict = DictFile(book)

		for word in self.dict.keys():
			iter = model.append()
			model.set(iter,
				0, word,
				1, self.dict[word].strip(),
				2, True)

	def selection_changed(self, widget, data = None):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			read(model.get_value(iter, 0))

class NewWord(gtk.VBox):
	def __init__(self, parent):
		gtk.VBox.__init__(self, False, 10)

		self.book = None

		main_hbox = gtk.HBox(False, 5)
		main_hbox.show()
		self.pack_start(main_hbox)

		self.wordlist = WordList(parent)
		self.wordlist.show()

		booklist = BookList(self.wordlist)
		booklist.show()

		self.wordlist.set_data("booklist", booklist)

		vbox = gtk.VBox(False, 10)
		vbox.show()
		main_hbox.pack_start(vbox, False, False, 0)

		sw = gtk.ScrolledWindow()
##		sw.set_size_request(200, -1)
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)
		sw.add(booklist)

		hbox = gtk.HBox(False, 5)
		hbox.show()
		vbox.pack_start(hbox, False, False, 0)

		button = gtk.Button(stock = gtk.STOCK_ADD)
		button.connect("clicked", self.on_add_book_clicked, booklist)
		button.show()
		hbox.pack_start(button)

		button = gtk.Button(stock = gtk.STOCK_REMOVE)
		button.connect("clicked", self.on_remove_book_clicked, booklist)
		button.show()
		hbox.pack_start(button)

		vbox = gtk.VBox(False, 10)
		vbox.show()
		main_hbox.pack_start(vbox)

		sw = gtk.ScrolledWindow()
		sw.show()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		hbox = gtk.HBox(False, 5)
		hbox.show()
		vbox.pack_start(hbox, False, False, 0)

		self.entry = gtk.Entry()
		self.entry.connect("activate", self.on_add_word, self.wordlist)
		self.entry.show()
		hbox.pack_start(self.entry)

		button = gtk.Button(stock = gtk.STOCK_FIND)
		button.connect("clicked", self.on_add_word, self.wordlist)
		button.show()
		hbox.pack_start(button, False, False, 0)

		sw.add(self.wordlist)
		self.show()

	def on_add_word(self, widget, wordlist):
		word_add = self.entry.get_text()
		books = ExistBook("/usr/share/reciteword/books") 
		cn = None 

		for book in books:
			if cn:
				break
			for word in file(book):
				if word.find("[W]" + word_add + "[T]") >= 0:
					cn = word.split('[W]')[1].split('[T]')[1].split('[M]')[1]
					break

		model = wordlist.get_model()
		iter = model.append()
		if cn:
			model.set(iter,
				COLUMN_EN, word_add,
				COLUMN_CN, cn.strip(),
				COLUMN_EDITABLE, True)
		else:
			model.set(iter,
				COLUMN_EN, word_add,
				COLUMN_CN, "在此输入中文解释",
				COLUMN_EDITABLE, True)

		wordlist.get_selection().select_iter(iter)
		wordlist.save(model)

	def on_add_book_clicked(self, widget, booklist):
		book_path = os.path.join(os.path.expanduser("~"), ".myword/books/", "myword-%s.bok" % datetime.datetime.today().isoformat(" ")[0:19])

		newbook = DictFile(book_path)
		newbook.INFO = {}
		newbook.INFO['FILE'] = book_path
		newbook.INFO['TITLE'] = "请输入书名"
		newbook.INFO['NUM'] = '0'
		newbook.INFO['AUTHOR'] = os.getenv("USERNAME")
		newbook.INFO['OTHER'] = 'auto-created by Myword-http://imtx.cn'
		newbook.save()

		model = booklist.get_model()
		iter = model.append()
		model.set(iter,
			COLUMN_TITLE, "在此输入书名",
			COLUMN_NUM, 0,
			COLUMN_PATH, book_path,
			COLUMN_EDITABLE_OF_BOOK, True)

	def on_remove_book_clicked(self, widget, booklist):
		dialog = MessageDialog("真的要删除吗？这是不可恢复的！")
		response = dialog.run()
		if response == gtk.RESPONSE_YES:
			model, iter = booklist.get_selection().get_selected()
			os.remove(model.get_value(iter, COLUMN_PATH))
			model.remove(iter)
		dialog.destroy()

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("NewWord")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = NewWord(win)
	vbox.show()
        win.add(vbox)

        win.show()
	gtk.main()
