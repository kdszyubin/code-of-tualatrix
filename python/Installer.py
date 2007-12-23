#!/usr/bin/env python

import gobject
import gtk
import apt_pkg

from xdg.DesktopEntry import DesktopEntry
from apt.package import Package

DESKTOP_DIR = '/usr/share/app-install/desktop/'
ICON_DIR = '/usr/share/app-install/icons/'

(
	COLUMN_INSTALLED,
	COLUMN_ICON,
	COLUMN_NAME
) = range(3)

data = \
(
	(False, "/usr/share/ubuntu-tweak/pixmaps/computer.png", 'pidgin'),
	(False, "/usr/share/ubuntu-tweak/pixmaps/computer.png", 'firefox'),
	(False, "/usr/share/ubuntu-tweak/pixmaps/startup.png", 'amsn')
)

class Installer(gtk.Window):
	def __init__(self, parent=None):
		# create window, etc
		gtk.Window.__init__(self)
		apt_pkg.init()
		self.cache = apt_pkg.GetCache()
		self.depcache = apt_pkg.GetDepCache(self.cache)
		self.records = apt_pkg.GetPkgRecords(self.cache)
		self.sourcelist = apt_pkg.GetPkgSourceList()

		self.set_title(self.__class__.__name__)
		self.connect("destroy", lambda *w: gtk.main_quit())
		self.set_border_width(8)
		self.set_default_size(300, 250)

		vbox = gtk.VBox(False, 8)
		self.add(vbox)

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		vbox.pack_start(sw)

		# create tree model
		model = self.__create_model()

		# create tree view
		treeview = gtk.TreeView(model)
		treeview.set_rules_hint(True)
		treeview.set_search_column(COLUMN_NAME)

		sw.add(treeview)

		# add columns to the tree view
		self.__add_columns(treeview)

		self.show_all()

	def __create_model(self):
		lstore = gtk.ListStore(
			gobject.TYPE_BOOLEAN,
			gtk.gdk.Pixbuf,
			gobject.TYPE_STRING)

		for item in data:
			iter = lstore.append()
			lstore.set(iter,
				COLUMN_INSTALLED, self.check_install(item[COLUMN_NAME]),
				COLUMN_ICON, gtk.gdk.pixbuf_new_from_file(item[COLUMN_ICON]),
				COLUMN_NAME, self.getName(item[COLUMN_NAME])
			)

		return lstore

	def check_install(self, name):
		pkgiter = self.cache[name]
		pkg = Package(self.cache, self.depcache, self.records, self.sourcelist, None, pkgiter)

		return pkg.isInstalled
	def getName(self, name):
		app = DesktopEntry(DESKTOP_DIR + name + ".desktop")
		return app.getName()

	def getIcon(self, name):
		app = DesktopEntry(DESKTOP_DIR + name + ".desktop")
		if app.getIcon().find("/") == 0:
			return DESKTOP_DIR + app.getIcon()
		else:
			return app.getIcon()

	def fixed_toggled(self, cell, path, model):
		# get toggled iter
		iter = model.get_iter((int(path),))
		fixed = model.get_value(iter, COLUMN_INSTALLED)

		# do something with the value
		fixed = not fixed

		# set new value
		model.set(iter, COLUMN_INSTALLED, fixed)

	def __add_columns(self, treeview):
		model = treeview.get_model()

		# column for fixed toggles
		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.fixed_toggled, model)

		column = gtk.TreeViewColumn(' ', renderer, active=COLUMN_INSTALLED)

		treeview.append_column(column)

		# column for application
		column = gtk.TreeViewColumn('Application')

		renderer = gtk.CellRendererPixbuf()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, pixbuf = COLUMN_ICON)

		renderer = gtk.CellRendererText()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, text = COLUMN_NAME)

		treeview.append_column(column)

def main():
	Installer()
	gtk.main()

if __name__ == '__main__':
	main()
