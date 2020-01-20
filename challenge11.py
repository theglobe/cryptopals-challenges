#!/usr/bin/env python3
from os import urandom
from random import randint, choice
from Crypto.Cipher import AES
from challenge8 import interblock_unique_chars_ratio
from challenge9 import pkcs7_pad

def encryption_oracle(input):
    prefix = bytes(urandom(randint(5,10)))
    suffix = bytes(urandom(randint(5,10)))
    to_encrypt = pkcs7_pad(prefix+input+suffix, 16)
    random_aes_key = urandom(16)

    if (choice([True, False])):
        cipher = AES.new(random_aes_key, AES.MODE_ECB)
        aes_mode='ECB'
    else:
        iv = urandom(16)
        cipher = AES.new(random_aes_key, AES.MODE_CBC, iv)
        aes_mode='CBC'
    
    ciphertext = cipher.encrypt(to_encrypt)
    return ciphertext, aes_mode

modes={}
modes['ECB'] = 0
modes['CBC'] = 0
num_correct = 0

# According to the challenge, I am allowed to specify which input goes
# into the oracle. Choose an input with repeated characters, that will
# lead to repeated ECB blocks
test_text = b'\x00' * 160

num_tests = 100000
for num in range(num_tests):
    ciphertext, mode = encryption_oracle(test_text)

    # My guess is that it's ECB if less than 0.5 of the characters
    # are unique
    num_unique = interblock_unique_chars_ratio(ciphertext, 16)
    if (num_unique < 0.5 and mode == 'ECB' or num_unique >= 0.5 and mode == 'CBC'): 
        num_correct += 1
    
    #print(len(ciphertext), num_unique, mode)
    modes[mode] += 1

print (modes)
print ("I detected ECB/CBC correctly in", num_correct / num_tests*100, "% of the cases")