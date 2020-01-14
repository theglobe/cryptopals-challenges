#!/usr/bin/env python3

import binascii
import sys

def repeating_key_xor(text,key):
	expanded_key = (key*(len(text)//len(key)+1))[:len(text)]
	xored = [a^ord(b) for (a,b) in zip(text,expanded_key)]
	return xored

if __name__ == "__main__":
	key = "ICE"
	text = bytes(sys.stdin.read(), 'ascii')
	xored = repeating_key_xor(text,key)
	print(binascii.hexlify(bytes(xored)))
