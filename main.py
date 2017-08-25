import os


from source.graph_reader import read_unlabelled_graph
from source.himesis_creator import *
from source.matching import *
from source.plotting import *

MAX_SIZE = 64

graph_dir = "./graphs"

graph_files = {}

print("Loading...")
for first in sorted(os.listdir(graph_dir)):

    if "graphsdb" in first:
        continue

    #print("First: " + first)

    for second in sorted(os.listdir(graph_dir + "/" + first)):
        #print("\tSecond: " + second)
        for third in sorted(os.listdir(graph_dir + "/" + first + "/" + second)):
            #print("\t\tThird: " + third)
            for graph_file in sorted(os.listdir(graph_dir + "/" + first + "/" + second + "/" + third)):
                print("\t\t\t" + graph_file)

                #if not "s16" in graph_file:
                #    continue

                graph_name = graph_file.split(".")[0] + "_" + graph_file.split(".")[1][-2:]
                graph_AB = graph_file.split(".")[1][0]

                graph_size = int(graph_file.split("_")[2].split(".")[0][1:])

                if graph_size > MAX_SIZE:
                    continue

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

print("Starting matching...")
times = {}
for k, v in graph_files.items():

    first = v[0]
    second = v[1]

    old_match_time = do_matching(k, first, second, use_new_matcher = False)
    new_match_time = do_matching(k, first, second, use_new_matcher = True)

    split_name = k.split("_")
    name = split_name[0] + "_" + split_name[1] + "_" + split_name[2]

    if name not in times.keys():
        times[name] = {"old" : [], "new" : []}

    times[name]["old"].append(old_match_time)
    times[name]["new"].append(new_match_time)

print("Starting plotting...")
plot_times(times)