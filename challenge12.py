#!/usr/bin/env python3
import base64, sys, string
from os import urandom
from random import randint, choice
from Cryptodome.Cipher import AES
from challenge8 import interblock_unique_chars_ratio
from challenge9 import pkcs7_pad

consistent_random_key = urandom(16)

def aes_encryption_oracle(text, key):
    # Given in the challenge
    secret_string = base64.b64decode(
    b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
    b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
    b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
    b'YnkK')

    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(text + secret_string, 16))

def discover_block_size(encryption_oracle):
    # Discover the block size
    lengths = []
    unique_ratio = []
    for length in range(48):
        my_string = b'A' * length
        ciphertext = encryption_oracle(my_string)
        lengths.append(len(ciphertext))
        unique_ratio.append(interblock_unique_chars_ratio(ciphertext, 16))

    unique_lengths = sorted(list(set(lengths)))
    diffs = set([b-a for (a,b) in zip(unique_lengths, unique_lengths[1:])])
    if (len(diffs) != 1):
        raise Exception('Could not determine a blocklength, got the candidates:', diffs)

    blocksize = list(diffs)[0]
    print('Determined block size to be', blocksize, 'bytes')

    # Detect that the function is using ECB
    # If unique_ratio is decresing with each added identical byte to the 
    # function, we can assume that it is ECB. A measure of this is that 
    # the last element substracted from the first gives a positive value
    diffs_num_unique = unique_ratio[0] - unique_ratio[-1]

    return blocksize, diffs_num_unique

def decrypt_appended(encryption_oracle):
    # Instead of doing exactly as in the challenge description, we will
    # make the initial padding of A's one byte short of the total encrypted
    # (padded) secret message. If we input an empty string to the oracle,
    # it will pad and encrypt just the secret message and we can start with
    # our initial padding (the A's) as one byte short of this. The rest goes
    # just as in the challenge description.

    # This method is a bit slower, since it needs to compare the whole length 
    # of the encrypted message to the test string, but it takes just a second 
    # in this case anyway.

    shortest = len(encryption_oracle(b''))
    target_size = shortest  
    input_block = b'A' * (target_size - 1)
    peek_encrypted = encryption_oracle(input_block)

    # Right after our crafted string now comes the first byte of the secret.
    # This string contains the cipher of the crafted string and the first byte:
    peek_block = peek_encrypted[:target_size-2]

    # We can now match it 
    decoded_chars = b''
    charpos = 0
    while(charpos < target_size-1):
        for char in range(257):
            if (char > 255):
                return decoded_chars

            test_block = input_block + bytes([char])
            encrypted = encryption_oracle(test_block)
            encrypted_block = encrypted[:target_size-2]
            assert(len(encrypted_block) == len(peek_block))

            if (encrypted_block == peek_block):
                decoded_chars += bytes([char])
                charpos += 1

                padding = b'A' * (target_size - 1 - charpos)
                input_block = padding + decoded_chars
                peek_encrypted = encryption_oracle(padding)
                peek_block = peek_encrypted[:target_size-2]
                assert(len(input_block) == target_size-1)
                break
    return decoded_chars

if __name__ == "__main__":
    oracle = lambda text: aes_encryption_oracle(text, consistent_random_key)

    blocksize, diffs_num_unique = discover_block_size(oracle)
    if (diffs_num_unique < 0):
        print('The function is not using ECB, exiting')
        sys.exit(0)

    # Now on to the attack
    decoded_chars = decrypt_appended(oracle)
    print(decoded_chars.decode('ascii'))
