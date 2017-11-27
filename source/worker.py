

from source.himesis_creator import *
import time
from multiprocessing import Process

from source.reading import read_unlabelled_graph
from source.matching import do_matching

from util.progress import ProgressBar

import os

class Worker(Process):

    def __init__(self, worker_id, verbosity, dir_queue, results_queue, match_counts, min_size, max_size):
        super(Worker, self).__init__()
        self.id = str(worker_id)
        self.dir_queue = dir_queue
        self.results_queue = results_queue
        self.match_counts = match_counts

        self.verbosity = verbosity

        self.min_size = min_size
        self.max_size = max_size

        self.progress_bar = None

        self.results_dir = "./results/times/"

    def run(self):

        print("Starting worker")

        while True:

            graph_dir = self.dir_queue.get()

            if graph_dir is None:
                break

            print("Worker " + self.id + ": " + graph_dir)

            start_time = time.time()
            graph_files = self.load_dir(graph_dir)
            end_time = time.time()

            print("Time taken for loading: " + str(end_time - start_time))

            self.match_graphs(graph_files)

            #self.print_times(times)
            #self.results_queue.put(times)

        print("Finished worker #" + self.id)

    def load_dir(self, graph_dir):

        graph_files = {}
        #print(graph_dir)

        for graph_file in sorted(os.listdir(graph_dir)):
            #print(graph_file)

            #print("\t\t\t" + graph_file)

            #if not "s16" in graph_file:
            #   continue

            name_split = graph_file.split(".")
            graph_name = name_split[0] + "_" + name_split[1][-2:]

            times_file = os.path.join(self.results_dir, graph_name[:-3] + ".times")
            if os.path.isfile(times_file):
                continue

            graph_AB = name_split[1][0]

            graph_size = int(graph_file.split("_")[2].split(".")[0][1:])

            if graph_size <= self.min_size:
                continue

            if graph_size > self.max_size > 0:
                continue

            #print(graph_name)
            #print(graph_AB)

            graph_filename = graph_dir + "/" + graph_file
            mx = read_unlabelled_graph(graph_filename)
            h = create_himesis(graph_file, mx)

            if graph_AB == "A":
                graph_files[graph_name] = [graph_file, h, None]
            elif graph_AB == "B":
                graph_files[graph_name][2] = h

        return graph_files

    def match_graphs(self, graph_files):
        print("Worker " + self.id + ": Starting matching of " + str(len(graph_files)) + " files...")
        times = {}

        if self.id == "0":

            self.progress_bar = ProgressBar(len(graph_files), prefix="Worker " + str(self.id) + " ")
        i = 0
        for k, v in graph_files.items():

            if self.progress_bar:
                self.progress_bar.update_progress(i)
            i += 1

            name = v[0]
            graph_A = v[1]
            graph_B = v[2]

            first_decompose, second_decompose = None, None

            try:
                match_count = self.match_counts[name]
            except KeyError:
                match_count = 0

            try:
                old_num_matches, old_match_time, _, _ = do_matching(name, graph_A, graph_B, match_count, use_new_matcher = False)
            except Exception as e:
                raise Exception("Old matcher Exception: " + str(e))
                old_num_matches = 0
                old_match_time = None

            try:
                new_num_matches, new_match_time, first_decompose, second_decompose = do_matching(name, graph_A, graph_B, match_count, use_new_matcher = True)
            except Exception as e:
                raise Exception("New matcher Exception: " + str(e))
                new_num_matches = 0
                new_match_time = None

            if old_num_matches != new_num_matches and old_match_time and new_match_time:
                print("Match count mismatch:")
                print(match_count)
                print(old_num_matches)
                print(new_num_matches)
                print("\n")

            split_name = k.split("_")
            name = split_name[0] + "_" + split_name[1] + "_" + split_name[2]

            if name not in times:
                times[name] = [[], [], [], [], 0, 0, 0]

            if old_match_time:
                times[name][0].append(old_match_time)
            else:
                times[name][4] += 1

            if new_match_time:
                times[name][1].append(new_match_time)
            else:
                times[name][5] += 1

            times[name][2].append(first_decompose)
            times[name][3].append(second_decompose)

            times[name][6] += 1

            if times[name][6] == 100:
                self.print_times(name, times)
        #return times

    def print_times(self, name, times):


        #for name in times.keys():
        with open(self.results_dir + name + ".times", 'w') as f:
            f.write(str(times[name][0]))
            f.write("\n")
            f.write(str(times[name][1]))
            f.write("\n")
            f.write(str(times[name][2]))
            f.write("\n")
            f.write(str(times[name][3]))
            f.write("\n")
            f.write(str(times[name][4]))
            f.write("\n")
            f.write(str(times[name][5]))
