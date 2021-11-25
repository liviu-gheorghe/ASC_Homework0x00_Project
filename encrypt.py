key=input()
input=open("text.txt", 'r')
text=input.read()
input.close()
output=open("encryptare.bin", 'w')
for i in range(len(text)):
    output.write(bin(ord(text[i])^ord(key[i%len(key)]))[2:].zfill(8))
output.close()