#!/usr/bin/env python

import os
import sys
import subprocess

def readword(word):
	if word:
		subprocess.Popen(["aplay","/usr/share/WyabdcRealPeopleTTS/%s/%s.wav" % (word[0], word)])

def typeword():
	subprocess.Popen(["aplay","/usr/share/reciteword/modules/type.wav"])

def delword():
	subprocess.Popen(["aplay","/usr/share/reciteword/modules/back.wav"])
	
	
if __name__ == "__main__":
	readword(sys.argv[1])
