from t_core.messages import Packet
from source.himesis_creator import create_matcher
import time
import timeout_decorator

@timeout_decorator.timeout(5 * 60, use_signals = False, )
def do_matching(name, first, second, match_count, use_new_matcher = False):
    first_matcher, first_decompose_time = create_matcher(name, first, new_matcher = use_new_matcher)

    # print(first_matcher)


    #print("Matching graphs: " + name + str(match_count))
    start_time = time.time()

    p = Packet()
    p.graph = second
    first_matcher.max = match_count
    first_matcher.packet_in(p)

    second_decompose_time = first_matcher.decomposing_time

    num_matches = len(p.match_sets)

    end_time = time.time()
    match_time = end_time - start_time

    if not first_matcher.is_success:
        raise Exception("Match not found!")
    # print(first_matcher.is_success)

    #print("Matching took " + str(match_time) + " seconds")

    return num_matches, match_time, first_decompose_time, second_decompose_time