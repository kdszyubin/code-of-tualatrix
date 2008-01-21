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
import cPickle as pickle

from widgets import MessageDialog, show_info
from dictfile import DictFile
from playsound import read
from UserList import UserList
from UserDict import UserDict

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

		selection = self.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed, list)
		if model.get_iter_first():
			selection.select_iter(model.get_iter_first())

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
	"""显示某一生词库的单词列表，其中parent参数是指主窗体，用于注册右键菜单
	sentence参数是例句，当选中一个单词时触发"""
	def __init__(self, parent, sentence):
		gtk.TreeView.__init__(self)

		self.book = None

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
		selection.connect("changed", self.selection_changed, sentence)

		menu = self.create_popup_menu(parent)
		menu.show_all()
		self.connect("button_press_event", self.button_press_event, menu)

	def on_cell_edited(self, cell, path_string, new_text, model):
		"""在编辑完单元格后触发，取得编辑前的文本，再比较编辑后的
		文本，并查找生词库中是否已存在编辑后的文本，假如条件满足则
		应用新的编辑，否则弹出对话框显示相关信息"""
		iter = model.get_iter_from_string(path_string)
		column = cell.get_data("column")
		old = model.get_value(iter, column)

		if self.get_reciting(old):
			dialog = MessageDialog('当前编辑的单词正在背诵中，不可更改' ,buttons = gtk.BUTTONS_OK)
			dialog.run()
			dialog.destroy()
		else:
			exist, exist_book = self.get_exist(new_text)

			if exist and new_text != old:
				dialog = MessageDialog('在"%s"中已经有"%s"这个单词了' % (DictFile(exist_book).INFO["TITLE"], new_text), buttons = gtk.BUTTONS_OK)
				dialog.run()
				dialog.destroy()
			else:
				model.set_value(iter, column, new_text)
				self.save(model)

	def get_reciting(self, word = None):
		"""取得当前编辑的单词是否正在背诵队列里，是则保护其不被修改"""
		f = file(os.path.join(os.path.expanduser("~"), ".myword/record"), "rb")
		
		Reciting = False
		Loading = True

		while Loading:
			try:
				rr = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				if word:
					if word in rr.words:
						Reciting = True
						break
				else:
					if self.book == rr.dict:
						Reciting = True
						break
		f.close()
		return Reciting

	def get_exist(self, new_word):
		"""判断当前加入的单词是否已存在, 返回一个tuple"""
		exist = False
		exist_book = None

		for book in os.listdir(os.path.join(os.path.expanduser("~"), ".myword/books")):
			if exist:
				break
			for word in file(os.path.join(os.path.expanduser("~"), ".myword/books", book)):
				if word.find("[W]" + new_word + "[M]") >= 0:
					exist_book = os.path.join(os.path.expanduser("~"), ".myword/books", book)
					exist = True
					break

		return exist, exist_book

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
		new.add_accelerator("activate", group, ord('N'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		new.connect("activate", self.add_new_word)
		remove = gtk.MenuItem("删除")
		remove.add_accelerator("activate", group, ord('D'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
		remove.connect("activate", self.remove_selected_word)
		
		menu.append(new)
		menu.append(remove)
		menu.attach_to_widget(self, None)

		return menu

	def add_new_word(self, widget, data = None):
		if self.book:
			model = self.get_model()
			iter = model.append()
			model.set(iter,
				COLUMN_EN, "在此输入英文",
				COLUMN_CN, "在此输入中文",
				COLUMN_EDITABLE, True)

			self.get_selection().select_iter(iter)

	def remove_selected_word(self, widget, data = None):
		"""当右键删除单库时触发，先判断是否在背诵，再进行移除，选
		中下一下，再更新生词库列表"""
		if self.get_selection().get_selected()[1]:
			model, iter = self.get_selection().get_selected()
			word = model.get_value(iter, COLUMN_EN)

			if self.get_reciting(word):
				dialog = MessageDialog('当前编辑的单词正在背诵中，不可更改' ,buttons = gtk.BUTTONS_OK)
				dialog.run()
				dialog.destroy()
			else:
				model.remove(iter)

				self.get_selection().select_iter(iter)

				self.save(model)

				booklist = self.get_data("booklist")
				model = booklist.get_model()
				booklist.update_list(model)

	def button_press_event(self, widget, event, data = None):
		if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
			data.popup(None, None, None, event.button, event.time)
		return False

	def update_list(self, book = None):
		model = self.get_model()
		model.clear()

		if book:
			self.book = book
			self.dict = DictFile(book)

			for word in self.dict.keys():
				iter = model.append()
				model.set(iter,
					0, word,
					1, self.dict[word].strip(),
					2, True)

	def selection_changed(self, widget, sentence):
		model = widget.get_selected()[0]
		iter = widget.get_selected()[1]
		if iter:
			word = model.get_value(iter, COLUMN_EN)
			sentence.set_display(word)
			read(word)

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

class SentenceBox(gtk.VBox):
	"""显示例句的窗口"""
	def __init__(self):
		gtk.VBox.__init__(self)
	
		self.word = ""

		eventbox = gtk.EventBox()
		eventbox.show()
		self.pack_start(eventbox, False, False, 5)

		self.label = gtk.Label("请选择一个单词")
		self.label.set_line_wrap(True)
		self.label.show()
		eventbox.add(self.label)

		self.hbox = gtk.HBox(False, 0)
		self.pack_start(self.hbox)

		self.entry = gtk.Entry()
		self.entry.show()
		self.entry.connect("activate", self.edit_finished)
		self.hbox.pack_start(self.entry)

		button = gtk.Button("Apply")
		button.show()
		button.connect("clicked", self.edit_finished)
		self.hbox.pack_start(button, False, False, 5)

		eventbox.connect("button_press_event", self.add_sentence)

	def add_sentence(self, widget, event, data = None):
		if event.type == gtk.gdk._2BUTTON_PRESS and self.word:
			self.label.hide()
			self.hbox.show()
			self.entry.grab_focus()

	def edit_finished(self, widget, data = None):
		sentence = SentenceFile()
		if self.entry.get_text():
			sentence[self.word] = self.entry.get_text()
			self.label.set_text(self.entry.get_text())
		else:
			if self.word in sentence:
				del sentence[self.word]
				self.set_display(self.word)
		self.label.show()
		self.hbox.hide()

	def set_display(self, word):
		self.label.show()
		self.hbox.hide()

		sentence = SentenceFile()
		self.word = word
		if word in sentence:
			self.label.set_label(sentence[word])
			self.entry.set_text(sentence[word])
		else:
			self.label.set_markup("<b>%s</b>还没有例句，请双击这里添加" % word)
			self.entry.set_text("")

class NewWord(gtk.VBox):
	def __init__(self, parent):
		gtk.VBox.__init__(self, False, 10)

		self.book = None

		main_hbox = gtk.HBox(False, 5)
		main_hbox.show()
		self.pack_start(main_hbox)

		#先创建例句的实例，即使它最后用到
		sentence = SentenceBox()
		sentence.show()

		self.wordlist = WordList(parent, sentence)
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

		vbox.pack_start(sentence, False, False, 5)

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
		new_word = self.entry.get_text()
		exist, exist_book = wordlist.get_exist(new_word)

		if new_word:
			if exist:
				dialog = MessageDialog('在"%s"中已经有"%s"这个单词了' % (DictFile(exist_book).INFO["TITLE"], new_word), buttons = gtk.BUTTONS_OK)
				dialog.run()
				dialog.destroy()
			else:
				books = ExistBook("books") 
				cn = None 

				for book in books:
					if cn:
						break
					for word in file(book):
						if word.find("[W]" + new_word + "[T]") >= 0:
							cn = word.split('[W]')[1].split('[T]')[1].split('[M]')[1]
							break

				model = wordlist.get_model()
				iter = model.append()
				if cn:
					model.set(iter,
						COLUMN_EN, new_word,
						COLUMN_CN, cn.strip(),
						COLUMN_EDITABLE, True)
				else:
					model.set(iter,
						COLUMN_EN, new_word,
						COLUMN_CN, "在此输入中文解释",
						COLUMN_EDITABLE, True)

				wordlist.get_selection().select_iter(iter)
				wordlist.save(model)
				widget.set_text("")

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
		if booklist.get_selection().get_selected()[1]:
			if self.wordlist.get_reciting():
				show_info("不能删除这本生词库，因为当前正在背诵队列里")
			else:
				dialog = MessageDialog("真的要删除吗？这是不可恢复的！")
				response = dialog.run()
				if response == gtk.RESPONSE_YES:
					model, iter = booklist.get_selection().get_selected()
					os.remove(model.get_value(iter, COLUMN_PATH))
					model.remove(iter)
					if model.get_iter_first():
						booklist.get_selection().select_iter(model.get_iter_first())
					else:
						self.wordlist.update_list()
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
