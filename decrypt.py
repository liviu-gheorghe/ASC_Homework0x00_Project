import sys
key=sys.argv[2]
fisierin=sys.argv[1]
fisierout=sys.argv[3]
input=open(fisierin, 'r+b')
output=open(fisierout, 'w', encoding='utf-8')
byte=input.read(1)
i=0
while byte:
    output.write(chr(ord(key[i%len(key)])^ord(byte)))
    byte=input.read(1)
    i=i+1
input.close()
output.close()
