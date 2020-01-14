#!/usr/bin/env python3

from Crypto.Cipher import AES
import base64

key = 'YELLOW SUBMARINE'

f = open('7.txt', 'r')
ciphertext = base64.b64decode(f.read())

cipher = AES.new(key, AES.MODE_ECB)
decoded = cipher.decrypt(ciphertext)

print(decoded.decode('ascii'))