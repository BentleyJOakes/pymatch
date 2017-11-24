import os
import binascii

def load_match_counts(graph_dir):
    match_counts = {}

    for count_file in sorted(os.listdir(graph_dir)):

        if not count_file.endswith(".gtr"):
            continue

        if not os.path.isfile(graph_dir + "/" + count_file):
            continue

        print("Reading file: " + count_file)
        with open(graph_dir + "/" + count_file) as f:
            for line in f.readlines():
                line = line.strip()
                s = line.split(" ")
                match_counts[s[0]] = int(s[1])

    return match_counts


def get_next_word(f):
    lower = f.read(1)
    higher = f.read(1)
    strHexLower = str(binascii.hexlify(lower),'utf-8')
    strHexHigher = str(binascii.hexlify(higher),'utf-8')
    return int(strHexHigher + strHexLower, 16)


def read_unlabelled_graph(filename):
    # print("Reading graph: " + filename)
    with open(filename, "rb") as f:
        length = get_next_word(f)

        mx = [[None for _ in range(length)] for _ in range(length)]

        # print(mx)
        for node in range(length):
            for _ in range(get_next_word(f)):
                mx[node][get_next_word(f)] = True
                # print(mx)

    return mx
