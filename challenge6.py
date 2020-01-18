#!/usr/bin/env python3

import base64
from challenge3 import find_single_byte_xor, score
from challenge5 import repeating_key_xor

def popcount(num):
	return bin(num).count('1')

def hamming_distance(bytes1,bytes2):
	xored = [(a)^(b) for (a,b) in zip(bytes1,bytes2)]
	return sum([popcount(x) for x in xored])

def find_key_lengths(ciphertext):
	"""
	Returns a list of tuples (edit_distance, keylength)
	"""
	average_distances = []
	for keysize in range(2,41):
		edit_distances = []
		blocks = [ciphertext[i:i+keysize] for i in range(0, len(ciphertext), keysize)]
		while (len(blocks) > 2):
			first = blocks[0]
			second = blocks[1]
			del blocks[0]
			del blocks[1]

			ed = hamming_distance(first, second) / keysize
			edit_distances.append(ed)
		average_distances.append((sum(edit_distances) / len(edit_distances), keysize))
	return average_distances

if __name__ == "__main__":
	print(hamming_distance(b'this is a test', b'wokka wokka!!!'))

	f = open('6.txt', 'r')
	ciphertext = base64.b64decode(f.read())

	average_distances = find_key_lengths(ciphertext)
	sorted_ed = sorted(average_distances, key=lambda tup: tup[0])
	print(sorted_ed)

	sizeindex=0
	keysize = sorted_ed[sizeindex][1]

	blocks = [ciphertext[i:i+keysize] for i in range(0, len(ciphertext), keysize)]

	key = []
	for keychar in range(0, keysize):
		blockchar = [(blocks[i][keychar]) for i in range(len(blocks)-1)]
		_, _, k = find_single_byte_xor(blockchar)
		key.append(k)

	keystr = ''.join([chr(k) for k in key])

	print (keystr)

	decoded = bytes(repeating_key_xor(ciphertext, keystr))
	print (decoded.decode('ascii'), score(decoded))
