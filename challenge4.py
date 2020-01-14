#!/usr/bin/env python3
import binascii
from challenge3 import *

file = open ("4.txt", "r")

maxscore = 0
winner = ""
for line in file:
	decoded,score,key = find_single_byte_xor(binascii.unhexlify(line.strip()))
	if (score > maxscore):
		winner = decoded
		maxscore = score

print (winner,maxscore)
