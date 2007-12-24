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
	(False, "/usr/share/ubuntu-tweak/pixmaps/startup.png", 'amsn'),
	(False, "/usr/share/ubuntu-tweak/pixmaps/startup.png", 'stardict'),
	(False, "/usr/share/ubuntu-tweak/pixmaps/startup.png", 'gftp'),
	(False, "/usr/share/ubuntu-tweak/pixmaps/startup.png", 'rar'),
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

		# create tree view
		treeview = self.create_treeview()
		treeview.set_rules_hint(True)
		treeview.set_search_column(COLUMN_NAME)

		sw.add(treeview)

		self.show_all()

	def check_install(self, name):
		pkgiter = self.cache[name]
		pkg = Package(self.cache, self.depcache, self.records, self.sourcelist, None, pkgiter)

		return pkg.isInstalled

	def getComment(self, name):
		app = DesktopEntry(DESKTOP_DIR + name + ".desktop")
		return app.getComment()

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

	def create_treeview(self):
		lstore = gtk.ListStore(
			gobject.TYPE_BOOLEAN,
			gtk.gdk.Pixbuf,
			gobject.TYPE_STRING)
		treeview = gtk.TreeView()

		# column for fixed toggles
		renderer = gtk.CellRendererToggle()
		renderer.connect('toggled', self.fixed_toggled, lstore)

		column = gtk.TreeViewColumn(' ', renderer, active=COLUMN_INSTALLED)

		treeview.append_column(column)

		# column for application
		column = gtk.TreeViewColumn('Application')

		renderer = gtk.CellRendererPixbuf()
		column.pack_start(renderer, True)
		column.set_attributes(renderer, pixbuf = COLUMN_ICON)

		renderer = gtk.CellRendererText()
		column.pack_start(renderer, True)
		#column.set_attributes(renderer, text = COLUMN_NAME)
		column.add_attribute(renderer, "markup", COLUMN_NAME)
		treeview.append_column(column)
		
		icon = gtk.icon_theme_get_default()

		for item in data:
			try:
				pixbuf = icon.load_icon(item[COLUMN_NAME], 24, 0)
			except gobject.GError:
				pixbuf = icon.load_icon(gtk.STOCK_MISSING_IMAGE, 24, 0)

			lstore.append((self.check_install(item[COLUMN_NAME]),
					pixbuf,
					"<big><b>%s</b></big>\n%s" % (self.getName(item[COLUMN_NAME]), self.getComment(item[COLUMN_NAME])),
					))
		
		treeview.set_model(lstore)

		return treeview

def main():
	Installer()
	gtk.main()

if __name__ == '__main__':
	main()
