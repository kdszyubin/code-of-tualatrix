#!/usr/bin/env python
# coding: utf-8

import gtk

def show_info(message, title = "提示", parent = None):
	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
	dialog.set_title(title)
	dialog.set_markup(message)
	dialog.run()
	dialog.destroy()
