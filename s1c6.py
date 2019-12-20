#!/usr/bin/env python3

def popcount(num):
	return bin(num).count('1')

def hamming_distance(str1,str2):
	xored = [ord(a)^ord(b) for (a,b) in zip(str1,str2)]
	return sum([popcount(x) for x in xored])

print(hamming_distance("this is a test", "wokka wokka!!!"))
