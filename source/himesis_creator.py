import os.path
import sys

sys.path.append(os.path.expanduser("~/Projects/SyVOLT/"))

from core.himesis import *
from core.himesis_utils import *

def create_himesis(name, mx):

    #print(mx)

    h = Himesis(name)

    length = len(mx)

    #add nodes
    for x in range(length):
        n = h.add_node()
        h.vs[n]["mm__"] = "node"

    for y, row in enumerate(mx):
        for x, col in enumerate(row):
            if mx[y][x]:
                h.add_edges([(x, y)])

    graph_to_dot(name, h)