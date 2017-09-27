

from source.himesis_creator import *
import time
from multiprocessing import Process

from source.reading import read_unlabelled_graph
from source.matching import do_matching

from util.progress import ProgressBar
MAX_SIZE = 196

class Worker(Process):

    def __init__(self, worker_id, verbosity, dir_queue, results_queue, match_counts):
        super(Worker, self).__init__()
        self.id = str(worker_id)
        self.dir_queue = dir_queue
        self.results_queue = results_queue
        self.match_counts = match_counts

        self.verbosity = verbosity

        self.progress_bar = None

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

            times = self.match_graphs(graph_files)

            self.print_times(times)
            #self.results_queue.put(times)

        print("Finished worker #" + self.id)

    def load_dir(self, graph_dir):

        graph_files = {}

        for graph_file in sorted(os.listdir(graph_dir)):

            #print("\t\t\t" + graph_file)

            #if not "s16" in graph_file:
            #   continue

            name_split = graph_file.split(".")
            graph_name = name_split[0] + "_" + name_split[1][-2:]
            graph_AB = name_split[1][0]

            graph_size = int(graph_file.split("_")[2].split(".")[0][1:])

            if graph_size > MAX_SIZE:
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
        print("Starting matching...")
        times = {}

        self.progress_bar = ProgressBar(len(graph_files), prefix="Worker " + str(self.id) + " ")
        i = 0
        for k, v in graph_files.items():

            self.progress_bar.update_progress(i)
            i += 1

            name = v[0]
            graph_A = v[1]
            graph_B = v[2]

            match_count = self.match_counts[name]

            old_num_matches, old_match_time = do_matching(name, graph_A, graph_B, match_count, use_new_matcher = False)
            new_num_matches, new_match_time = do_matching(name, graph_A, graph_B, match_count, use_new_matcher = True)

            if old_num_matches != new_num_matches:
                print("Match count mismatch:")
                print(match_count)
                print(old_num_matches)
                print(new_num_matches)
                print("\n")

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
                f.write(str(times[name][0]))
                f.write("\n")
                f.write(str(times[name][1]))