#!/usr/bin/env python
# coding: utf-8

import os
import gtk
import gobject
import cPickle as pickle
from UserDict import UserDict

(
	COLUMN_NAME,
	COLUMN_PROGRESS,
	COLUMN_TASKOBJECT,
) = range(3)

class MessageDialog(gtk.MessageDialog):

	def __init__(self, 
			message,
			title = "提示",
			parent = None, 
			flags = 0, 
			type = gtk.MESSAGE_INFO,
			buttons = gtk.BUTTONS_YES_NO):
		gtk.MessageDialog.__init__(self, parent, flags, type, buttons)
		self.set_markup(message)
		self.set_title(title)

class TaskFile(UserDict):
	"""任务文件"""
	def __init__(self, name = None):
		UserDict.__init__(self)

class TaskEditDialog(gtk.Dialog):
	"""添加或编辑任务的对话框, name参数即代表编辑，否则新加"""
	def __init__(self, name = None):
		gtk.Dialog.__init__(self)

		lbl1 = gtk.Label ("标题:");
		lbl2 = gtk.Label ("当前量:");
		lbl3 = gtk.Label ("总量:");

		self.task_name = gtk.Entry ();
		self.task_current = gtk.Entry ();
		self.task_total = gtk.Entry ();

		if name:
			self.task_name.set_text(name)

			f = file(os.path.join(os.path.expanduser("~"), ".myprogress/record"), "rb")
			Loading = True
			while Loading:
				try:
					task = pickle.load(f)
				except pickle.UnpicklingError:
					pass
				except EOFError:
					Loading = False
				else:
					if task['name'] == name:
						self.task_current.set_text(task['current'])
						self.task_total.set_text(task['total'])

		table = gtk.Table(3, 2)
		table.attach(lbl1, 0, 1, 0, 1)
		table.attach(lbl2, 0, 1, 1, 2)
		table.attach(lbl3, 0, 1, 2, 3)
		table.attach(self.task_name, 1, 2, 0, 1)
		table.attach(self.task_current, 1, 2, 1, 2)
		table.attach(self.task_total, 1, 2, 2, 3)

		self.vbox.pack_start(table)

		self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
		self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)

		self.set_default_response(gtk.RESPONSE_OK)

		self.show_all()

class TaskView(gtk.TreeView):
	"""任务列表的视图"""
	def __init__(self):
		gtk.TreeView.__init__(self)

		model = self.__create_model()
		self.set_model(model)

		self.set_rules_hint(True)
		self.__add_columns()

		self.update_model()
	
	def __create_model(self):
		lstore = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_INT,
			gobject.TYPE_PYOBJECT)

		return lstore

	def __add_columns(self):
		model = self.get_model()

		column = gtk.TreeViewColumn('任务名', gtk.CellRendererText(), text=COLUMN_NAME)
		self.append_column(column)

		column = gtk.TreeViewColumn('进度', gtk.CellRendererProgress(), value=COLUMN_PROGRESS)
		self.append_column(column)

	def update_model(self):
		"""更新数据模块"""
		model = self.get_model()
		model.clear()

		f = file(os.path.join(os.path.expanduser("~"), ".myprogress/record"), "rb")
		Loading = True
		while Loading:
			try:
				task = pickle.load(f)
			except pickle.UnpicklingError:
				pass
			except EOFError:
				Loading = False
			else:
				percent = float(task['current']) / float(task['total']) * 100
				iter = model.append()
				model.set(iter,
					COLUMN_NAME, task['name'],
					COLUMN_PROGRESS, percent,
					COLUMN_TASKOBJECT, task)

		f.close()

class MyProgress(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)

		self.connect('destroy', lambda *w: gtk.main_quit())
		self.set_title(self.__class__.__name__)
		self.set_position(gtk.WIN_POS_CENTER)
		self.config_test()

		self.set_border_width(8)
		self.set_default_size(500, 350)

		vbox = gtk.VBox(False, 8)
		self.add(vbox)

		label = gtk.Label('这里是你的工程')
		vbox.pack_start(label, False, False)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		self.treeview = TaskView()
		sw.add(self.treeview)

		hbox = gtk.HBox(False, 0)
		vbox.pack_start(hbox, False, False, 10)

		selection = self.treeview.get_selection()
		selection.set_mode(gtk.SELECTION_SINGLE)
		selection.connect("changed", self.selection_changed)
		
		button = gtk.Button(stock = gtk.STOCK_ADD)
		button.connect("clicked", self.on_add_button, self.treeview)
		hbox.pack_start(button, True, False, 0)

		button = gtk.Button(stock = gtk.STOCK_EDIT)
		button.connect("clicked", self.on_edit_button, self.treeview)
		hbox.pack_start(button, True, False, 0)

		button = gtk.Button(stock = gtk.STOCK_DELETE)
		button.connect("clicked", self.on_delete_button, self.treeview)
		hbox.pack_start(button, True, False, 0)

		self.show_all()

	def selection_changed(self, widget, data = None):
		model, iter = widget.get_selected()
		if iter:
			self.task = model.get_value(iter, COLUMN_TASKOBJECT)

	def get_progress(self, task):
		return float(task['current']) / float(task['total']) * 100

	def on_delete_button(self, widget, treeview):
		dialog = MessageDialog("警告！你真的要删除你的任务吗？", type = gtk.MESSAGE_WARNING)
		response = dialog.run()	
		if response == gtk.RESPONSE_YES:
			model, iter = treeview.get_selection().get_selected()
			model.remove(iter)
			self.save()
		dialog.destroy()

	def on_edit_button(self, widget, treeview):
		dialog = TaskEditDialog(self.task['name'])
		response = dialog.run()	
		if response == gtk.RESPONSE_OK:
			model, iter = treeview.get_selection().get_selected()
			task = model.get_value(iter, COLUMN_TASKOBJECT)
			task['name'] = dialog.task_name.get_text()
			task['total'] = dialog.task_total.get_text()
			task['current'] = dialog.task_current.get_text()

			model.set(iter, COLUMN_NAME, task['name'],
					COLUMN_PROGRESS, self.get_progress(task),
					COLUMN_TASKOBJECT, task)
			self.save()
		dialog.destroy()

	def on_add_button(self, widget, treeview):
		dialog = TaskEditDialog()
		response = dialog.run()	
		if response == gtk.RESPONSE_OK:
			task = TaskFile()
			task['name'] = dialog.task_name.get_text()
			task['total'] = dialog.task_total.get_text()
			task['current'] = dialog.task_current.get_text()
			model = treeview.get_model()
			iter = model.append()
			model.set(iter, COLUMN_NAME, task['name'],
						COLUMN_PROGRESS, self.get_progress(task),
						COLUMN_TASKOBJECT, task)
			self.save()
		dialog.destroy()

        def config_test(self):
		"""检测配置文件是否存在，否则创建之"""
                home_dir = os.path.join(os.path.expanduser("~"), ".myprogress"
)
                record_file = os.path.join(home_dir, "record")

                if not os.path.exists(home_dir):
                        os.makedirs(home_dir)

                if not os.path.exists(record_file):
                        f = file(record_file, "wb")
                        f.close()

	def save(self):
		"""保存文件"""
		model = self.treeview.get_model()
		iter = model.get_iter_first()

		f = file(os.path.join(os.path.expanduser("~"), ".myprogress/record"), "wb")

		while iter:
			task = model.get_value(iter, COLUMN_TASKOBJECT)
			pickle.dump(task, f, True)
			iter = model.iter_next(iter)
		f.close()

def main():
	MyProgress()
	gtk.main()

if __name__ == '__main__':
	main()
