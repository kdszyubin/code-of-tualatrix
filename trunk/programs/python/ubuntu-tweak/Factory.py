#!/usr/bin/env python
import UserDict
from Widgets import GconfCheckButton
from SystemInfo import SystemInfo
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class XmlHandler(ContentHandler):
        def __init__(self, dict):
		self.dict = dict

        def startElement(self, name, attrs):
                if name == "item":
			try:
				minor = attrs["version"]
			except KeyError:
				self.dict[attrs["title"]] = attrs["key"]
			else:
				if SystemInfo.gnome.minor == minor:
					self.dict[attrs["title"]] = attrs["key"]

class GconfKeys:
	"""This class used to store the keys, it will create for only once"""
	keys = {}
	parser = make_parser()
	handler = XmlHandler(keys)
	parser.setContentHandler(handler)
	parser.parse("tweaks.xml")

class Factory:
	keys = GconfKeys.keys
	def create(self, widget = None, label = None, key = None, tooltip = None):
		return getattr(self, "create_%s" % widget)(label, key, tooltip)
	
	def create_gconfcheckbutton(self, label, key, tooltip = None):
		if key in self.keys:
			button = GconfCheckButton(label, self.keys[key])
			if tooltip:
				button.set_tooltip_text(tooltip)
			return button
		else:
			return None

if __name__ == "__main__":
	print Factory().keys
