import sys
key=sys.argv[1]
fisierin=sys.argv[2]
fisierout=sys.argv[3]
input=open(fisierin, 'r', encoding='utf-8')
text=input.read()
coduri=[]
for i in range(len(text)):
    coduri.append(ord(text[i]))
input.close()
for i in range(len(coduri)):
    coduri[i]=coduri[i]^ord(key[i%len(key)])
output=open(fisierout, 'w+b')
coduri=bytearray(coduri)
output.write(coduri)
output.close()