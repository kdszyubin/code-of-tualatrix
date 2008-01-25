#!/usr/bin/env python

import gtk
import gobject

(
	COLUMN_TITLE,
	COLUMN_PROGRESS,
) = range(2)

data = \
(
	("hello", 33),
	("hello", 95),
)

class MyProgress(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		self.connect('destroy', lambda *w: gtk.main_quit())
		self.set_title(self.__class__.__name__)

		self.set_border_width(8)
		self.set_default_size(300, 250)

		vbox = gtk.VBox(False, 8)
		self.add(vbox)

		label = gtk.Label('This is the bug list (note: not based on real data')
		vbox.pack_start(label, False, False)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		model = self.__create_model()

		treeview = gtk.TreeView(model)
		treeview.set_rules_hint(True)

		sw.add(treeview)

		self.__add_columns(treeview)

		self.show_all()

	def __create_model(self):
		lstore = gtk.ListStore(
			gobject.TYPE_STRING,
			gobject.TYPE_INT)

		for item in data:
			iter = lstore.append()
			lstore.set(iter,
				COLUMN_TITLE, item[COLUMN_TITLE],
				COLUMN_PROGRESS, item[COLUMN_PROGRESS])
		return lstore

	def __add_columns(self, treeview):
		model = treeview.get_model()

		column = gtk.TreeViewColumn('Title', gtk.CellRendererText(), text=COLUMN_TITLE)
		treeview.append_column(column)

		column = gtk.TreeViewColumn('Progress', gtk.CellRendererProgress(), value=COLUMN_PROGRESS)
		treeview.append_column(column)

def main():
	MyProgress()
	gtk.main()

if __name__ == '__main__':
	main()
