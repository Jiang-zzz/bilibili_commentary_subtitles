import sys
import re
import xml.etree.ElementTree as ET
from crc32_crack import hash_to_id


def find_user(xml_file_name, frequency):
    tree = ET.parse(xml_file_name)
    root = tree.getroot()
    xml_str = ET.tostring(root, encoding="unicode")

    match = re.findall(r"\"(.+?)\"", xml_str)

    hash_list = []
    for text in match:
        hash_list.append(text.split(",")[6])

    hash_count = {}
    for hash_code in hash_list:
        if hash_code in hash_count:
            hash_count[hash_code] += 1
        else:
            hash_count[hash_code] = 1

    frequent_users_hash = {
        hash_code: count for hash_code, count in hash_count.items() if count > frequency
    }

    frequent_hash_list = frequent_users_hash.keys()
    hash_count_list = [(k, frequent_users_hash[k]) for k in frequent_hash_list]

    id_hash_count_list = hash_to_id(hash_count_list)
    id_hash_count_list.sort(key=lambda x: x[2], reverse=True)

    address_head = "https://space.bilibili.com/"
    address_count_list = [
        tuple([f"{address_head}{id_}", hash_code, count])
        for id_, hash_code, count in id_hash_count_list
    ]
    return address_count_list


if __name__ == "__main__":
    xml_file_name = sys.argv[1]
    frequency = int(sys.argv[2])
    find_user(xml_file_name, frequency)
    results = find_user(xml_file_name, frequency)
    for result in results:
        print(result)
