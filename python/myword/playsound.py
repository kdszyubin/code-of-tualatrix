#!/usr/bin/env python

# Myword - Python based word recite application
#
# Copyright (C) 2008 TualatriX <tualatrix@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import sys
import subprocess

def read(word):
	if word:
		subprocess.Popen(["aplay","/usr/share/WyabdcRealPeopleTTS/%s/%s.wav" % (word[0], word)])

def play(type):
	subprocess.Popen(["aplay","sound/%s.wav" % type])

if __name__ == "__main__":
	read(sys.argv[1])
