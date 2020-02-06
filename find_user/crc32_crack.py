import sys
import time

CRCPOLYNOMIAL = 0xEDB88320
crctable = [0 for x in range(256)]


def create_table():
    for i in range(256):
        crcreg = i
        for _ in range(8):
            if (crcreg & 1) != 0:
                crcreg = CRCPOLYNOMIAL ^ (crcreg >> 1)
            else:
                crcreg = crcreg >> 1
        crctable[i] = crcreg


def crc32(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return crcstart


def crc32_last_index(string):
    crcstart = 0xFFFFFFFF
    for i in range(len(str(string))):
        index = (crcstart ^ ord(str(string)[i])) & 255
        crcstart = (crcstart >> 8) ^ crctable[index]
    return index


def get_crc_index(t):
    for i in range(256):
        if crctable[i] >> 24 == t:
            return i
    return -1


def deep_check(i, index):
    string = ""
    tc = 0x00
    hashcode = crc32(i)
    tc = hashcode & 0xFF ^ index[2]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[2]] ^ (hashcode >> 8)
    tc = hashcode & 0xFF ^ index[1]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[1]] ^ (hashcode >> 8)
    tc = hashcode & 0xFF ^ index[0]
    if not (tc <= 57 and tc >= 48):
        return [0]
    string += str(tc - 48)
    hashcode = crctable[index[0]] ^ (hashcode >> 8)
    return [1, string]


def main(string):
    index = [0 for x in range(4)]
    i = 0
    ht = int(f"0x{string}", 16) ^ 0xFFFFFFFF
    for i in range(3, -1, -1):
        index[3 - i] = get_crc_index(ht >> (i * 8))
        snum = crctable[index[3 - i]]
        ht ^= snum >> ((3 - i) * 8)
    for i in range(100000000):
        lastindex = crc32_last_index(i)
        if lastindex == index[3]:
            deepCheckData = deep_check(i, index)
            if deepCheckData[0]:
                break
    if i == 100000000:
        return -1
    return f"{i}{deepCheckData[1]}"


def hash_to_id(hash_count_list):
    create_table()
    hash_dic = {}
    id_count_list = []
    for hash_code, count in hash_count_list:
        if hash_dic.get(hash_code) is None:
            id_ = main(hash_code)
            hash_dic[hash_code] = id_
        else:
            id_ = hash_dic[hash_code]
        id_count_list.append(tuple([id_, count]))

    return id_count_list


# if __name__ == "__main__":
#     create_table()
#     start_time = time.time()
#     print(main(sys.argv[1]))
#     end_time = time.time()
#     print(f"耗时: {round(end_time - start_time, 2)}秒")
