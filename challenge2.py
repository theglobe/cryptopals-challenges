import binascii

hex1 = "1c0111001f010100061a024b53535009181c"
hex2 = "686974207468652062756c6c277320657965"

bin1 = binascii.unhexlify(hex1)
bin2 = binascii.unhexlify(hex2)
#bin1 = bytes.fromhex(hex1)
#bin2 = bytes.fromhex(hex2)

print(bin1)
print(bin2)

list = [ chr(a ^ b) for (a,b) in zip(bin1, bin2) ] 
xored = str.encode("".join(list))

print (binascii.b2a_hex(xored))
