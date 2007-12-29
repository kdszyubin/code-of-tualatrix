#!/usr/bin/env python

import gtk
import gobject
import os

class BookList(gtk.TreeView):
	def __init__(self, dir):
		gtk.TreeView.__init__(self)

		model = gtk.TreeStore(gobject.TYPE_STRING)
		iter = model.append(None)
		self.__create_model(dir, model, iter)

		self.set_model(model)
		self.__add_columns()

	def __create_model(self, dir, model, iter):
		for item in os.listdir(dir):
			fullname = os.path.join(dir, item)
			print fullname
			if os.path.isdir(fullname):
				child_iter = model.append(iter)
				dirnamefile = os.path.join(fullname, "dirname")
				print "    Set father:%s\n " % dirnamefile
				model.set(child_iter, 0, dirnamefile)

				for subitem in os.listdir(fullname):
					subfullname = os.path.join(fullname, subitem)
					if os.path.isdir(subfullname):
						child_iter = model.append(iter)
						self.__create_model(subfullname, model, child_iter)
#					elif os.path.basename(subfullname) != "dirname":
#						child_iter = model.append(iter)
#						print "    (nodirname)Set child: %s" % subitem
#						model.set(child_iter, 0, subfullname)
			else:
				child_iter = model.append(iter)
				print "    Set child: %s\n" % fullname 
				model.set(child_iter, 0, fullname)

	def __add_columns(self):
		model = self.get_model()

		renderer = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Directory", renderer, text = 0)

		self.append_column(column)

if __name__ == "__main__":
	win = gtk.Window()
	win.connect('destroy', lambda *w: gtk.main_quit())
        win.set_title("BookList TreeView")
        win.set_default_size(650, 400)
        win.set_border_width(8)

        vbox = gtk.VBox(False, 8)
        win.add(vbox)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw)

        # create treeview
        treeview = BookList("/usr/share/reciteword/books")
#        treeview.set_rules_hint(True)

        sw.add(treeview)

        win.show_all()
	gtk.main()
