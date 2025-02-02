#!/usr/bin/env python3
from urllib import parse
from os import urandom
from Cryptodome.Cipher import AES
from challenge9 import pkcs7_pad
from challenge12 import discover_block_size, decrypt_appended

def parse_string(text):
    return dict(parse.parse_qs(parse.urlsplit(text).path))

def profile_for(text_email):
    value = {}
    value['email'] = text_email
    value['uid'] = 10
    value['role'] = "user"
    return parse.urlencode(value)

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pkcs7_pad(text, 16))

def decrypt(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(text)

consistent_random_key = urandom(16)

def oracle(email):
    profile = bytes(profile_for(email), 'ascii')
    return encrypt(profile, consistent_random_key)

# A. Encrypt the encoded user profile under the key; 
# # "provide" that to the "attacker".
profile_enc = oracle("foo@bar.com")
print (profile_enc)

# B. Decrypt the encoded user profile and parse it.
profile_dec = decrypt(profile_enc, consistent_random_key)
print (profile_dec)

# Using only the user input to profile_for() (as an oracle 
# to generate "valid" ciphertexts) and the ciphertexts 
# themselves, make a role=admin profile. 

blocksize, diffs_num_unique = discover_block_size(oracle)
print (blocksize, diffs_num_unique)

appended=decrypt_appended(oracle)
print(appended)