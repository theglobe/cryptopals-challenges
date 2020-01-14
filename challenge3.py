#!/usr/bin/env python3
import binascii

def xor_decode(bin, keyval):
	xored = [a ^ keyval for a in bin]
	return bytes(xored)

def score(text):
	score=0
	for s in list(text.upper()):
		if (chr(s) in "ETAOIN"):
			score +=1
		elif (s != 9 and s != 10 and s != 13 and s < 32 or s > 127):
			score -= 10
	return 1. * score / len(text)

def find_single_byte_xor(encrypted):
	maxscore=-32000
	winner=""
	key=None
	for i in range(0,255):
		decoded = (xor_decode(encrypted, i))

		thisscore=score(decoded)
		#if (thisscore > 70) : print (i, thisscore, decoded)
		if (thisscore>maxscore):
			maxscore=thisscore
			winner=decoded
			key=i
	return winner,maxscore,key

if __name__ == "__main__":
	encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

	decoded, maxscore, key = find_single_byte_xor(binascii.unhexlify(encrypted)) 
	print((decoded), maxscore, key)
