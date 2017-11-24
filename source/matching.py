import sys
from t_core.messages import Packet
from source.himesis_creator import create_matcher
import time
#import timeout_decorator

#@timeout_decorator.timeout(20 * 60, use_signals = False, )
def do_matching(name, first, second, match_count, use_new_matcher = False):
    first_matcher, first_decompose_time = create_matcher(name, first, new_matcher = use_new_matcher)

    # print(first_matcher)

    old_recursion_limit = sys.getrecursionlimit()
    expected_max_recursion_level = first.vcount() + second.vcount()
    if old_recursion_limit < 1.5 * expected_max_recursion_level:
        sys.setrecursionlimit(int(1.5 * expected_max_recursion_level))


    #print("Matching graphs: " + name + str(match_count))
    start_time = time.time()

    p = Packet()
    p.graph = second
    first_matcher.max = match_count

    try:
        first_matcher.packet_in(p)
    except RuntimeError as e:
        raise Exception("Runtime Error - Matching failed! " + str(e))
    except Exception as e:
        raise Exception("Matching failed! " + str(e))


    second_decompose_time = first_matcher.decomposing_time

    num_matches = len(p.match_sets)

    end_time = time.time()
    match_time = end_time - start_time

    if not first_matcher.is_success:
        raise Exception("Match not found! " + name)
    # print(first_matcher.is_success)

    #print("Matching took " + str(match_time) + " seconds")

    return num_matches, match_time, first_decompose_time, second_decompose_time
