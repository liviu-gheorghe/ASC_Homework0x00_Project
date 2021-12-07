f = open("output_adversa", "rb")

bin_data = f.read()

def hammingDist(bs1, bs2):

    dist = 0
    for byte_tuple in zip(bs1, bs2):
        x = byte_tuple[0] ^ byte_tuple[1]
        sb_count = 0
        while x > 0:
            sb_count += x & 1
            x = x >> 1
        dist += sb_count

    return dist


def getKeylen(bin_data):


    lowest_dist = None
    best_keylen = None

    for klen in range (10, 16):


        chunk_count = 0
        start  = 0
        end = start + klen
        current_dist = 0

        while(start < len(bin_data)) :

            bitgroup_1 = bin_data[start:end]
            bitgroup_2  = bin_data[start+klen:end + klen]

            current_dist += hammingDist(bitgroup_1, bitgroup_2) / klen
            chunk_count += 1
            start += klen
            end += klen

        current_dist = current_dist / chunk_count
        #print("Average hamming distance for keylen = {} is {}".format(klen, current_dist))

        if lowest_dist is None or current_dist < lowest_dist:
            lowest_dist = current_dist
            best_keylen = klen

    return best_keylen


def getDataGroups(bin_data, keylen):
    dict_data = {}
    i = 0
    for byte in bin_data:
        dict_key = i % keylen
        if dict_key not in dict_data:
            dict_data[dict_key] = []

        dict_data[i%keylen].append(byte)
        i += 1

    return dict_data


keylen = getKeylen(bin_data)
dct = getDataGroups(bin_data, keylen)
best_key = ''

def getKeyUsingFreqAnalysis(bin_data):
    global best_key
    most_common = "eEiIaArRtTnN oOcCsSlLuUmM0123456789"

    for dataGroup in dct.values():

        best_char = None
        best_score = 0


        xored_bits = []
        for j in range(127):
            cc_score = 0
            xored_bits = [j ^ current_bit for current_bit in dataGroup]

            xored_bits = bytes(xored_bits)
            xored_bits = str(xored_bits, 'utf-8')
            

            for xored_char in xored_bits:
                if xored_char in most_common:
                    cc_score += 1

            if cc_score > best_score:
                best_score = cc_score
                best_char = chr(j)

        best_key += best_char

getKeyUsingFreqAnalysis(bin_data)
print("Cheia folosita este \"{}\"".format(best_key))
