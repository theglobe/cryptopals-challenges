#!/usr/bin/env python3

from Crypto.Cipher import AES
import base64
from challenge9 import pkcs7_pad

def xor(block1, block2):
    assert len(block1) == len(block2)
    return bytes([a ^ b for (a,b) in zip(block1,block2)])

def aes_cbc_encrypt(plaintext, key, iv):
    blocksize = 16
    prev_block = iv

    ciphertext = b''
    blocks = [plaintext[i:i+blocksize] for i in range(0, len(plaintext), blocksize)]

    # Mode is ECB, no cheating :)
    cipher = AES.new(key, AES.MODE_ECB)

    for block in blocks:
        if (len(block) < blocksize):
            block = pkcs7_pad(block, blocksize)
        combined_block = xor(block, prev_block)
        cipher_block = cipher.encrypt(combined_block)
        prev_block = cipher_block
        ciphertext += cipher_block
    
    return ciphertext

def aes_cbc_decrypt(ciphertext, key, iv):
    blocksize = 16
    prev_block = iv

    plaintext = b''
    blocks = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]

    cipher = AES.new(key, AES.MODE_ECB)

    for cipher_block in blocks:
        combined_block = cipher.decrypt(cipher_block)
        block = xor(combined_block, prev_block)
        prev_block = cipher_block
        plaintext += block
    
    return plaintext

if __name__ == "__main__":
    key = 'YELLOW SUBMARINE'
    iv = b'\x00' * 16

    f = open('10.txt', 'r')
    ciphertext = base64.b64decode(f.read())
    decrypted = aes_cbc_decrypt(ciphertext, key, iv)
    print (decrypted.decode('ascii'))
