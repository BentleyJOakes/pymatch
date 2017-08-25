
from t_core.messages import Packet
from source.himesis_creator import *
import time

def do_matching(name, first, second, use_new_matcher = False):
    first_matcher = create_matcher(name, first, new_matcher = use_new_matcher)

    # print(first_matcher)


    #print("Matching graphs: " + k)
    start_time = time.time()

    p = Packet()
    p.graph = second
    first_matcher.max = 1
    first_matcher.packet_in(p)

    end_time = time.time()
    match_time = end_time - start_time

    if not first_matcher.is_success:
        raise Exception("Match not found!")
    #print(first_matcher.is_success)

    #print("Matching took " + str(match_time) + " seconds")

    return match_time