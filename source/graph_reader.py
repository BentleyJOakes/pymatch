def get_next_word(f):
    lower = f.read(1)
    higher = f.read(1)
    both = higher.hex() + lower.hex()
    return int(both, 16)

def read_unlabelled_graph(filename):
    print(filename)
    with open(filename, "rb") as f:
        length = get_next_word(f)

        mx = [[None for y in range(length)] for x in range(length)]

        #print(mx)
        for node in range(length):
            num_edges = get_next_word(f)
            for edge in range(num_edges):
                target = get_next_word(f)
                mx[node][target] = True
        #print(mx)

    return mx
