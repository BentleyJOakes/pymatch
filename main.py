import os

from source.graph_reader import read_unlabelled_graph
from source.himesis_creator import *

from t_core.messages import Packet
from t_core.matcher import Matcher
from t_core.iterator import Iterator

graph_dir = "./graphs"

graph_files = {}

for first in sorted(os.listdir(graph_dir)):

    if "graphsdb" in first:
        continue

    #print("First: " + first)

    for second in sorted(os.listdir(graph_dir + "/" + first)):
        #print("\tSecond: " + second)
        for third in sorted(os.listdir(graph_dir + "/" + first + "/" + second)):
            #print("\t\tThird: " + third)
            for graph_file in sorted(os.listdir(graph_dir + "/" + first + "/" + second + "/" + third)):
                #print("\t\t\t" + graph_file)

                if not "s16" in graph_file:
                    continue

                graph_name = graph_file.split(".")[0] + "_" + graph_file.split(".")[1][-2:]
                graph_AB = graph_file.split(".")[1][0]

                #print(graph_name)
                #print(graph_AB)

                graph_filename = graph_dir + "/" + first + "/" + second + "/" + third + "/" + graph_file
                mx = read_unlabelled_graph(graph_filename)
                h = create_himesis(graph_file.split("/")[-1], mx)

                if graph_AB == "A":
                    graph_files[graph_name] = [h, None]
                elif graph_AB == "B":
                    graph_files[graph_name][1] = h

            break
        break
    break


for k, v in graph_files.items():
    print("Matching graphs: " + k)
    first = v[0]
    second = v[1]

    first_matcher = create_matcher(k, first)

    #print(first_matcher)

    p = Packet()
    p.graph = second
    first_matcher.max = 1
    first_matcher.packet_in(p)

    print(first_matcher.is_success)
