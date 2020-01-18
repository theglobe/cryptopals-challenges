#!/usr/bin/env python3

def pkcs7_pad(text, length):
    if (length <= 0):
        raise ValueError("Length must be strictly positive")
    padlen = length - len(text) % length
    return text + bytes([padlen]) * padlen

if __name__ == "__main__":
    text = b'YELLOW SUBMARINE'
    print (pkcs7_pad(text, 20))
