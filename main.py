import os
import sys
sys.path.append(os.path.expanduser("~/Projects/SyVOLT/"))

from source.worker import Worker
from source.reading import load_match_counts

import multiprocessing
from multiprocessing import Manager, Queue

verbosity = 0


MIN_SIZE = 0
MAX_SIZE = 4000

if len(sys.argv) > 1:
    MIN_SIZE = int(sys.argv[1])
if len(sys.argv) > 2:
    MAX_SIZE = int(sys.argv[2])


graph_dir = "./graphs"

match_counts = load_match_counts(graph_dir + "/graphsdb/")

print("Starting matching")
print("Min: " + str(MIN_SIZE))
print("Max: " + str(MAX_SIZE))

do_parallel = True

if do_parallel:
    cpu_count = multiprocessing.cpu_count()
    print("CPU Count: " + str(cpu_count))
else:
    cpu_count = 1
    print("Restricting to one thread")

manager = Manager()
dir_queue = manager.Queue()
results_queue = manager.Queue()

workers = []

for i in range(cpu_count):
    new_worker = Worker(i, verbosity, dir_queue, results_queue, match_counts, min_size=MIN_SIZE, max_size=MAX_SIZE)
    workers.append(new_worker)

for worker in workers:
    worker.start()

print("Loading...")
for first in sorted(os.listdir(graph_dir)):

    if "graphsdb" in first or ".git" in first:
        continue

    #print("First: " + first)

    for second in sorted(os.listdir(graph_dir + "/" + first)):
        #print("\tSecond: " + second)

        #if "bvg" in second:
        #    continue

        for third in sorted(os.listdir(graph_dir + "/" + first + "/" + second)):
            #third_dir = graph_dir + "/" + first + "/" + second + "/" + third
            #print("\t\tDir: " + third_dir)

            worker_dir = graph_dir + "/" + first + "/" + second + "/" + third
            dir_queue.put(worker_dir)


for i in range(len(workers)):
    dir_queue.put(None)

for worker in workers:
    worker.join()

#
# for worker in workers:
#     result = results_queue.get()
#     print(result)

#print("Starting plotting...")
#plot_times(times)