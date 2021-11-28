import sys
key=sys.argv[1]
fisierin=sys.argv[2]
fisierout=sys.argv[3]
input=open(fisierin, 'rb')
coduri=[]
i = 0
while byte := input.read(1):
    enc_byte = ord(byte)
    enc_byte = enc_byte ^ ord(key[i%len(key)])
    coduri.append(enc_byte)
    i += 1
input.close()
output=open(fisierout, 'w+b')
coduri=bytearray(coduri)
output.write(coduri)
output.close()
