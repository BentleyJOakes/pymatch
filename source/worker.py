

from source.himesis_creator import *
import time
from multiprocessing import Process

from source.reading import read_unlabelled_graph
from source.matching import do_matching

class Worker(Process):

    def __init__(self, worker_id, verbosity, dir_queue, results_queue):
        super(Worker, self).__init__()
        self.id = str(worker_id)
        self.dir_queue = dir_queue
        self.results_queue = results_queue
        self.verbosity = verbosity

    def run(self):

        print("Starting worker")

        while True:

            graph_dir = self.dir_queue.get()

            if graph_dir is None:
                break

            print("Worker " + self.id + ": " + graph_dir)

            graph_files = self.load_dir(graph_dir)
            times = self.match_graphs(graph_files)

            self.print_times(times)
            #self.results_queue.put(times)

    def load_dir(self, graph_dir):

        graph_files = {}

        for graph_file in sorted(os.listdir(graph_dir)):

            #print("\t\t\t" + graph_file)

            if not "s16" in graph_file:
                continue

            graph_name = graph_file.split(".")[0] + "_" + graph_file.split(".")[1][-2:]
            graph_AB = graph_file.split(".")[1][0]

            #graph_size = int(graph_file.split("_")[2].split(".")[0][1:])

            #if graph_size > MAX_SIZE:
            #    continue

            #print(graph_name)
            #print(graph_AB)

            graph_filename = graph_dir + "/" + graph_file
            mx = read_unlabelled_graph(graph_filename)
            h = create_himesis(graph_file.split("/")[-1], mx)

            if graph_AB == "A":
                graph_files[graph_name] = [h, None]
            elif graph_AB == "B":
                graph_files[graph_name][1] = h

        return graph_files

    def match_graphs(self, graph_files):
        print("Starting matching...")
        times = {}

        for k, v in graph_files.items():

            first = v[0]
            second = v[1]

            old_match_time = do_matching(k, first, second, use_new_matcher = False)
            new_match_time = do_matching(k, first, second, use_new_matcher = True)

            split_name = k.split("_")
            name = split_name[0] + "_" + split_name[1] + "_" + split_name[2]

            if name not in times:
                times[name] = [[], []]

            times[name][0].append(old_match_time)
            times[name][1].append(new_match_time)

        return times

    def print_times(self, times):
        results_dir = "./results/times/"

        for name in times.keys():
            with open(results_dir + name + ".times", 'w') as f:
                f.write(str(times[name]))