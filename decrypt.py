import sys
key=sys.argv[2]
fisierin=sys.argv[1]
fisierout=sys.argv[3]
input=open(fisierin, 'r+b')
output=open(fisierout, 'w', encoding='utf-8')
byte=input.read(1)
result_bytes = b""
i=0
while byte:
    dec_byte = ord(key[i%len(key)])^ord(byte)
    is_nl = False
    if dec_byte == 0x0A:
        is_nl = True
    dec_byte = dec_byte.to_bytes(1,byteorder='big')
    result_bytes += dec_byte
    if is_nl:
        output.write(result_bytes.decode())
        result_bytes = b""
    byte=input.read(1)
    i=i+1
input.close()
output.write(result_bytes.decode())
output.close()
