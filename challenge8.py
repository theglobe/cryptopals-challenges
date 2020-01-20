#!/usr/bin/env python3

import binascii

def interblock_unique_chars_ratio(text, blocklength):
    blocks = [text[i:i+blocklength] for i in range(0, len(text), blocklength)]
    num_unique = 0
    for index in range(blocklength):
        chars = [blocks[block_index][index] for block_index in range(len(blocks))]
        num_unique += len(set(chars))
    return num_unique/len(text)

if __name__ == "__main__":
    f = open('8.txt', 'r')

    lowest_num_unique = 32000
    line_nr = 0
    for line in f.readlines():
        line_nr += 1
        ciphertext = binascii.unhexlify(line.strip())
        num_unique = interblock_unique_chars_ratio(ciphertext, 16)

        print(line_nr, num_unique)
        if (num_unique < lowest_num_unique):
            lowest_num_unique = num_unique
            detected_ecb = ciphertext
            line_nr_ecb = line_nr

    blocks = [detected_ecb[i:i+16] for i in range(0, len(detected_ecb), 16)]
    for block in blocks:
        print(block)

    print (lowest_num_unique, line_nr_ecb)