import os.path
import sys

sys.path.append(os.path.expanduser("~/Projects/SyVOLT/"))

from core.himesis import *
from core.himesis_utils import *

from pyramify.PyRamify import *

def create_himesis(name, mx):

    #print(mx)
    name = name.replace(".", "_")

    h = Himesis(name)
    h["mm__"] = ['HimesisMM']
    h["name"] = name
    h['GUID__'] = nprnd.randint(9223372036854775806)
    h["equations"] = []

    length = len(mx)

    edges = []

    #add nodes
    for x in range(length):
        n = h.add_node()
        h.vs[n]["mm__"] = "node"

    for y, row in enumerate(mx):
        for x, col in enumerate(row):
            if mx[y][x]:
                edges.append((x, y))

    h.add_edges(edges)

    mn = h.add_node()
    h.vs[mn]["mm__"] = "MatchModel"

    an = h.add_node()
    h.vs[an]["mm__"] = "ApplyModel"

    pwn = h.add_node()
    h.vs[pwn]["mm__"] = "paired_with"

    edges = [(mn, pwn), (pwn, an)]
    for x in range(length):
        edges.append((mn, x))

    h.add_edges(edges)

    #graph_to_dot(name, h)
    return h

def create_matcher(name, graph):

    rd = {name : graph}

    #print(graph)

    out_dir = "./patterns/"
    file_name = graph.compile(out_dir)
    #graph_to_dot(name, graph)

    pyram = PyRamify(draw_svg=False)
    matcher_dict = pyram.get_match_pattern(rd)

    matcher = list(matcher_dict.values())[0]
    return matcher

