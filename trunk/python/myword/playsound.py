#!/usr/bin/env python

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
