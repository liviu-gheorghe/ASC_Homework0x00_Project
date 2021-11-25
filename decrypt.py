import sys

sys_args = sys.argv

key = sys_args[2]
input=open(sys_args[1], 'r')
output=open(sys_args[3], 'w')
decryption=[]
i=0
while bin:
    bin=input.read(8)
    nr=0
    exp=7
    for digit in bin:
        if digit=='1':
            nr=nr+2**exp
        exp=exp-1
    decryption.append(chr(nr^ord(key[i%len(key)])))
    i=i+1
input.close()
decryption.pop()
decryption=''.join(decryption)
output.write(decryption)
output.close()

