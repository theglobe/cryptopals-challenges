#!/usr/bin/env python3

import binascii

from challenge6 import find_key_lengths

f = open('8.txt', 'r')

lowest_ed = 32000
line_nr = 0
for line in f.read().split('\n'):
    line_nr += 1
    ciphertext = binascii.unhexlify(line.strip())

    if len(ciphertext) > 1:
        # Re-using this is a bit overkill since we only need one of the elements
        # in the list it returns.
        average_distances = find_key_lengths(ciphertext)

        # The edit distance of the 16 byte blocks is the 14th element in this list
        ed = average_distances[14][0]
        if (ed < lowest_ed):
            lowest_ed = ed
            detected_ecb = ciphertext
            line_nr_ecb = line_nr

print (lowest_ed, line_nr_ecb)

blocks = [detected_ecb[i:i+16] for i in range(0, len(detected_ecb), 16)]
for block in blocks:
    print(block)
