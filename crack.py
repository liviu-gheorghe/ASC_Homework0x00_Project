import math
import sys

f = open("input_adversa.txt", "rb")
g = open("output_adversa", "rb")
h = open("cheie.txt", "w")

while byteg := g.read(1):
    bytef = f.read(1)
    cc = ord(byteg) ^ ord(bytef)
    h.write(chr(cc))

f.close()
g.close()
h.close()

key = ""
h = open("cheie.txt", "r")
text = h.read()

def getKey(text):

    global key
    chunk_count = len(text) // (10 if "--fpc" in sys.argv else 1)
    while (chunk_count >= 1):
        it_l = 0
        it_r = math.floor(len(text)/chunk_count) * chunk_count
        chunk_len = it_r // chunk_count

        if text[:chunk_len] * chunk_count ==  text[it_l:it_r]:
            key = text[:chunk_len]
            return
        chunk_count -= 1

getKey(text)
print("Cheia folosita este \"{}\"".format(key))
