#!/usr/bin/env python3
import base64, sys, string
from os import urandom
from random import randint, choice
from Crypto.Cipher import AES
from challenge8 import interblock_unique_chars_ratio
from challenge9 import pkcs7_pad

def aes_encryption_oracle(text, key):
    # Given in the challenge
    secret_string = base64.b64decode(
    b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
    b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
    b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
    b'YnkK')

    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(text + secret_string, 16))

consistent_random_key = urandom(16)

# Discover the block size
lengths = []
unique_ratio = []
for length in range(48):
    my_string = b'A' * length
    ciphertext = aes_encryption_oracle(my_string, consistent_random_key)
    lengths.append(len(ciphertext))
    unique_ratio.append(interblock_unique_chars_ratio(ciphertext, 16))

unique_lengths = sorted(list(set(lengths)))
diffs = set([b-a for (a,b) in zip(unique_lengths, unique_lengths[1:])])
if (len(diffs) != 1):
    print('Could not determine a blocklength, got the candidates:', diffs)
    sys.exit(0)
blocksize = list(diffs)[0]
print('Determined block size to be', blocksize, 'bytes')

# Detect that the function is using ECB
# If unique_ratio is decresing with each added identical byte to the 
# function, we can assume that it is ECB. A measure of this is that 
# the last element substracted from the first gives a positive value
diffs_num_unique = unique_ratio[0] - unique_ratio[-1]
if (diffs_num_unique < 0):
    print('The function is not using ECB, exiting')
    sys.exit(0)

# Now on to the attack

shortest = len(aes_encryption_oracle(b'', consistent_random_key))
target_length = shortest + blocksize -1
one_byte_short = b'A' * (blocksize - 1)
one_byte_short_encrypted = aes_encryption_oracle(one_byte_short, consistent_random_key)

# Right after our crafted string now comes the first byte of the secret.
# This string contains the cipher of the crafted string and the first byte:
first_bytes_of_cipher = one_byte_short_encrypted[:blocksize-2]

# We can now match it 
decoded_chars = []
charpos = 0
while(charpos < blocksize):
    for char in range(257):
        if (char > 255):
            print("Some error")
            print(one_byte_short)
            print(bytes(decoded_chars))
            print(charpos)
            sys.exit(0)

        input_block = one_byte_short + bytes([char])
        encrypted = aes_encryption_oracle(input_block, consistent_random_key)
        encrypted_block = encrypted[:blocksize-2+charpos]
        assert(len(encrypted_block) == len(first_bytes_of_cipher))

        if (encrypted_block == first_bytes_of_cipher):
            print(char)
            decoded_chars.append(char)
            charpos += 1

            one_byte_short = one_byte_short + bytes([char])
            one_byte_short_encrypted = aes_encryption_oracle(one_byte_short, consistent_random_key)
            first_bytes_of_cipher = one_byte_short_encrypted[:blocksize-2+charpos]
            assert(len(first_bytes_of_cipher) == blocksize+charpos-2)
            break

print(bytes(decoded_chars))
