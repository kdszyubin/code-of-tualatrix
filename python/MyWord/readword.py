#!/usr/bin/env python

import os
import sys
import subprocess

def readword(word = None, type = None):
	if type:
		subprocess.Popen(["aplay", "/usr/share/reciteword/modules/type.wav"])
	else:
		subprocess.Popen(["aplay","/usr/share/WyabdcRealPeopleTTS/%s/%s.wav" % (word[0], word)])

if __name__ == "__main__":
	readword(sys.argv[1])
