import sys



sys_args = sys.argv

key=sys_args[1]
input=open(sys_args[2], 'r')
text=input.read()
input.close()
output=open(sys_args[3], 'w')
for i in range(len(text)):
    output.write(bin(ord(text[i])^ord(key[i%len(key)]))[2:].zfill(8))
output.close()
