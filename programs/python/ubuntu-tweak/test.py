#!/usr/bin/env python
# coding: utf-8

import gtk
import gconf
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

class Setting:
	client = gconf.client_get_default()

	def __init__(self, key):
		self.key = key

		dir = self.get_dir_from_key(key)
		self.client.add_dir(dir, gconf.CLIENT_PRELOAD_NONE)
		self.client.notify_add(key, self.value_changed, key)

		self.value = self.client.get(key)

		self.value_type = ''

	def value_changed(self, client, id, entry, data = None):
		print "我靠！有变化了！"

	def get_dir_from_key(self, key):
		return "/".join(key.split("/")[0: -1])

class XmlLoader(ContentHandler):
	def __init__(self):
		pass

	def startElement(self, name, attrs):
		if name == "item":
			print "Start:", name, attrs["title"]
			print "Start:", name, attrs["key"]
		else:
			print "Start:", name, attrs

	def endElement(self, name):
		print "End:", name
	
	def characters(self, text):
		pass

if __name__ == "__main__":
	Setting("/apps/panel/global/confirm_panel_remove")
	Setting("/apps/panel/global/locked_down")
	gtk.main()
