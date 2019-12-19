#!/usr/bin/env python3
import binascii

encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def xor_decode(bin, keyval):
	list = [ chr(a ^ keyval) for a in bin]
	xored = str.encode("".join(list))
	return xored

def score(text):
	score=0
	for s in text.upper():
		if (chr(s) in "ETAOIN"):
			score +=1
	return score

def find_single_byte_xor(encrypted):
	maxscore=0
	winner=""
	key=None
	for i in range(0,255):
		decoded = (xor_decode(binascii.unhexlify(encrypted), i))
	#	print (decoded.upper())
	#	if ((decoded.upper() != decoded.lower()) and decoded.find(b' ')>-1):
		thisscore=score(decoded)
		if (thisscore>maxscore):
			maxscore=thisscore
			winner=decoded
			key=i
	return winner,maxscore,key

if __name__ == "__main__":
	decoded, maxscore, key = find_single_byte_xor(encrypted) 
	print(decoded, maxscore, key)
