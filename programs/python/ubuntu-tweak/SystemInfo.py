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
pygtk.require('2.0')
from xml.sax import make_parser
from xml.dom import minidom

class GnomeVersion:
	xmldoc = minidom.parse("/usr/share/gnome-about/gnome-version.xml")

	platform = xmldoc.getElementsByTagName("platform")[0].firstChild.data
	minor = xmldoc.getElementsByTagName("minor")[0].firstChild.data
	micro = xmldoc.getElementsByTagName("micro")[0].firstChild.data
	distributor = xmldoc.getElementsByTagName("distributor")[0].firstChild.data
	date = xmldoc.getElementsByTagName("date")[0].firstChild.data

	def __str__(self):
		return "%s.%s.%s (%s %s)" % (self.platform, self.minor, self.micro, self.distributor, self.date)

class DistroInfo:
	if GnomeVersion.distributor == "Ubuntu":
		from aptsources import distro
		ubuntu = distro.get_distro()
		distribution = ubuntu.description
		codename = ubuntu.codename

class SystemInfo:
	gnome = GnomeVersion()
			
if __name__ == "__main__":
	print SystemInfo.gnome