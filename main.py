from source.graph_reader import read_unlabelled_graph
from source.himesis_creator import *

graph_file = "/home/dcx/Projects/pymatch/graphs/graphsdb/iso/m2D/m2D/iso_m2D_m196.A00"

mx = read_unlabelled_graph(graph_file)

h = create_himesis(graph_file.split("/")[-1], mx)