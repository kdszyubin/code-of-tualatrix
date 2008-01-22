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
import os

try:
	from gnome import url_show
except ImportError:
	pass
from revise import Revise
from choosebook import ChooseBook
from firstrecite import FirstRecite
from widgets import show_info
from result import Result
from newword import NewWord

VERSION = "0.9.6"

class MyWord(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.config_test()

		self.set_title("Myword " + VERSION)
		self.set_icon_from_file("myword.png")
		self.set_size_request(560, 320)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("destroy", lambda *w: gtk.main_quit())

		vbox = gtk.VBox(False, 0)
		vbox.show()
		self.add(vbox)

		self.notebook = gtk.Notebook()
		self.notebook.show()
		self.notebook.set_tab_pos(gtk.POS_LEFT)
		vbox.pack_start(self.notebook)

		welcome = self.welcome()
		welcome.show_all()
		label = gtk.Label("欢迎")
		self.notebook.append_page(welcome, label)

		label = gtk.Label("选书")
		self.notebook.append_page(ChooseBook(self), label)

		self.firstrecite = self.create_firstrecite()
		self.firstrecite.show()
		label = gtk.Label("初记")
		self.notebook.append_page(self.firstrecite, label)

		label = gtk.Label("复习")
		self.notebook.append_page(Revise(), label)

		label = gtk.Label("生词")
		self.notebook.append_page(NewWord(self), label)

		self.result = Result()
		self.result.show_all()
		label = gtk.Label("成绩")
		self.notebook.append_page(self.result, label)

		about = self.welcome(message = """
\tMyword是一款基于PyGTK的背单词软件，它使用ReciteWord的词库，并支持它的语音库。\n\n\tMyword具备完整的单词测试、词义回想和复习功能，并应用了记忆遗忘曲线，按时提醒你复习。你可以随时查看当前的背诵状态，因为Myword提供了详细的信息可供追踪。\n\t除此之外，Myword还拥有强大的生词库功能，无论背不背单词，都可以用Myword来创建并管理自己的生字库。查看其他信息请点击我""", 
				size = "large", about = True)
		about.show_all()
		label = gtk.Label("关于")
		self.notebook.append_page(about, label)

		self.show()

		self.notebook.connect("switch-page", self.switch_page_cb)

	def switch_page_cb(self, widget, page, page_num, data = None):
		if page_num == 5:
			self.result.create_model()

	def config_test(self):
		home_dir = os.path.join(os.path.expanduser("~"), ".myword/books")
		record_file = os.path.join(os.path.expanduser("~"), ".myword/record")
		finished_file = os.path.join(os.path.expanduser("~"), ".myword/finished")
		sentence_file = os.path.join(os.path.expanduser("~"), ".myword/sentence")

		if not os.path.exists(home_dir):
			os.makedirs(home_dir)

		if not os.path.exists(record_file):
			f = file(record_file, "wb")
			f.close()

		if not os.path.exists(finished_file):
			f = file(finished_file, "wb")
			f.close()

		if not os.path.exists(sentence_file):
			f = file(sentence_file, "wb")
			f.close()

	def welcome(self, message = "欢迎使用Myword背单词软件！", size = "xx-large", about = None):
		vbox = gtk.VBox(False, 10)

		eventbox = gtk.EventBox()
		if about:
			eventbox.connect("button_press_event", self.show_about)
		vbox.pack_start(eventbox)

		label = gtk.Label()
		label.set_line_wrap(True)
		label.set_markup('<span size="%s">%s</span>' % (size, message))
		eventbox.add(label)

		return vbox

	def click_website(self, dialog, link, data = None):
		url_show(link)

	def show_about(self, widget, event, data =  None):
		gtk.about_dialog_set_url_hook(self.click_website)

		about = gtk.AboutDialog()
		about.set_icon_from_file("myword.png")
		about.set_name("Myword")
		about.set_version(VERSION)
		about.set_website("http://imtx.cn")
		about.set_website_label("I'm TualatriX!")
		about.set_logo(gtk.gdk.pixbuf_new_from_file("myword.png"))
		about.set_comments("基于PyGTK的背单词软件！词库来自ReciteWord.")
		about.set_authors(["TualatriX <tualatrix@gmail.com>"])
		about.set_copyright("Copyright © 2008 TualatriX")
		about.set_wrap_license(True)
		about.set_license("Myword is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.\n\
Myword is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\
You should have received a copy of the GNU General Public License along with Ubuntu Tweak; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA")
		about.run()
		about.destroy()

	def create_firstrecite(self, book = None):
		return FirstRecite(book)

def main():
	MyWord()
	gtk.main()

if __name__ == "__main__":
	main()
