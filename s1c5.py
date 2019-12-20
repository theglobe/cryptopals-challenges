#!/usr/bin/env python3

import binascii
import sys

def repeating_key_xor(text,key):
	expanded_key = (key*(len(text)//len(key)+1))[:len(text)]
	xored = [ord(a)^ord(b) for (a,b) in zip(text,expanded_key)]
	return binascii.hexlify(bytearray(xored))

key = "ICE"
text = sys.stdin.read()
xored = repeating_key_xor(text,key)
print(xored)
