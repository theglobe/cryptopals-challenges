import base64
import binascii

hexdata = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

def hexToBase64(hexdata):
	binary = binascii.unhexlify(hexdata)
	return base64.b64encode(binary)

print(hexToBase64(hexdata))
