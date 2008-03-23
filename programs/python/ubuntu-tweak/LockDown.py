#!/usr/bin/env python

# Ubuntu Tweak - PyGTK based desktop configure tool
#
# Copyright (C) 2007-2008 TualatriX <tualatrix@gmail.com>
#
# Ubuntu Tweak is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ubuntu Tweak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import pygtk
pygtk.require("2.0")
import gtk
import os
import gconf
import gettext

from Factory import Factory
from Widgets import ListPack

gettext.install("ubuntu-tweak", unicode = True)

lockdown_keys = \
[
	"disable_command_line",
	"disable_lock_screen",
	"disable_printing",
	"disable_print_setup",
	"disable_save_to_disk",
	"disable_user_switching",
	"disable_user_switchingg",
]

lockdown_names = \
[
	_("Disable \"Run Application\" dialog (Alt+F2)"),
	_("Disable Lock Screen"),
	_("Disable Printing"),
	_("Disable Print Setup"),
	_("Disable Save To Disk"),
	_("Disable User Switching"),
	_("Disable User Switchingg"),
]

class LockDown(gtk.VBox):
        """Lock down some function"""

        def __init__(self):
                gtk.VBox.__init__(self)

		box = ListPack(_("<b>System Security options</b>"), ())
		for key in lockdown_keys:
			button = Factory.create("gconfcheckbutton", lockdown_names[lockdown_keys.index(key)], key, "Hello Wolrd!")
			if button:
				box.vbox.pack_start(button, False, False, 0)
#			button = GConfCheckButton(lockdown_names[lockdown_keys.index(key)], key)

		self.pack_start(box, False, False, 0)

if __name__ == "__main__":
	from Utility import Test
        Test(LockDown)
