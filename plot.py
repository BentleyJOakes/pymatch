import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from collections import defaultdict
import os


import random

class Plotter:

    def __init__(self):
        self.decompose_times = defaultdict(list)
        self.decompose_times_types = defaultdict(lambda: defaultdict(list))

        self.old_matching_times = defaultdict(list)
        self.new_matching_times = defaultdict(list)

        self.old_failures = defaultdict(int)
        self.new_failures = defaultdict(int)

        self.old_matching_times_types = defaultdict(lambda: defaultdict(list))
        self.new_matching_times_types = defaultdict(lambda: defaultdict(list))

        self.old_matcher_colour = '#dd2233'
        self.old_matcher_colour2 = "0.75"

        self.new_matcher_colour = "#2233dd"
        self.new_matcher_colour2 = "1.00"

        self.max_time = 20 * 60
        self.max_time_line = "#333333"

        self.figure_size_x, self.figure_size_y = 18.5, 10.5
        self.figure_dpi = 150

    def plot_times(self, times_file, old_times, new_times):

        name = times_file.replace(".times","")

        print("Plotting: " + name)
        #data = np.array((times[key]['old'], times[key]['new']))
        #data = np.rot90(data)

        labels = ['Old Matcher','New Matcher']
        fs = 10  # fontsize
        plt.figure()
        #data = np.random.lognormal(size = (37, 4), mean = 1.5, sigma = 1.75)

        #fig = plt.boxplot(data, showmeans=True, meanline=True)
        #fig.set_title('Times', fontsize = fs)

        #plt.plot(data['old'], range(100), data['new'], range(100))
        #t = np.arange(0., 5., 0.2)

        # red dashes, blue squares and green triangles
        #plt.plot(range(100), times[key]['old'], 'r*', range(100), times[key]['new'], 'bs',)

        data = [old_times, new_times]
        plt.boxplot(data, labels = labels, showmeans = True, meanline = True)

        plt.ylabel('Time (s)')
        plt.yscale('log')
        plt.title("Times for: " + name)
        #plt.show()

        results_dir = "results/"
        plt.savefig(results_dir + "/" + name + '.png', bbox_inches = 'tight')
        plt.close()





    def plot_decompose_times(self):
        print("Creating decompose time graph...")
        name = "decompose_times"
        labels = sorted(self.decompose_times_types.keys())

        print(labels)
        fig = plt.figure()
        fig.set_size_inches(self.figure_size_x, self.figure_size_y)



        for label in labels:
            #print(self.decompose_times_types[label].keys())

            data_x = []
            data_y = []
            for size in list(self.decompose_times_types[label].keys()):

                for d_times in list(self.decompose_times_types[label].values())[0]:

                    data_x.append(size)
                    data_y.append(d_times)

            #print(data_x)
            #print(data_y)
            plt.plot(data_x, data_y, marker=".", linestyle='None', color='black', label=label[:3])


        # data = [list(self.decompose_times[k]) for k in sorted(self.decompose_times.keys())]
        # plt.boxplot(data, labels = labels, showmeans = True, meanline = True, sym = '+')
        plt.xlabel('Graph size')
        plt.ylabel('Time (s)')
        plt.title("Time for Decomposing During Matching")
        #plt.legend(bbox_to_anchor=(0.98, 0.15))
        results_dir = "results/"
        plt.savefig(results_dir + "/abc_" + name + '.png', bbox_inches = 'tight', dpi = self.figure_dpi)
        plt.close()

    def plot_matching_times(self, old_times, new_times, suffix):
        print("Creating matching time graph " + suffix + "...")
        name = "matching_times" + suffix

        fig = plt.figure()
        fig.set_size_inches(self.figure_size_x, self.figure_size_y)


        x_ticks = []

        rand_spread = 20
        do_old = False
        size_max = 550

        # i = 0.5
        old_buckets = defaultdict(list)
        new_buckets = defaultdict(list)

        def get_bucket_name(k):
            return k[:3] #+ k[-2:]

        def reject(k):
            return False#"si2m3D" not in k

        if do_old:
            for k in sorted(old_times.keys()):
                if reject(k):
                    continue

                bucket_name = get_bucket_name(k)

                for x in old_times[k]:
                    if x > size_max and "iso" not in k:
                        continue

                    x_ticks.append(x)

                    for y in old_times[k][x]:
                        rand = random.randrange(-rand_spread, rand_spread)
                        old_buckets[bucket_name].append((x + rand, y))

            for k in old_buckets:
                print(k)
                c, v = zip(*old_buckets[k])

                plt.plot(c, v, marker=".", linestyle='None', label=k)

        else:
            for k in sorted(new_times.keys()):
                if reject(k):
                    continue

                bucket_name = get_bucket_name(k)
                for x in new_times[k]:
                    if x > size_max and "iso" not in k:
                        continue

                    x_ticks.append(x)
                    for y in new_times[k][x]:
                        rand = random.randrange(-rand_spread, rand_spread)
                        new_buckets[bucket_name].append((x + rand, y))

            for k in new_buckets:
                print(k)
                c, v = zip(*new_buckets[k])

                plt.plot(c, v, marker=".", linestyle='None', label=k)

        # print(old_buckets)





        #     data = [old_times[k], new_times[k]]
        #
        #     dividing_line = i+1.5
        #     plt.axvline(dividing_line, ls = "-", color = "0.75")
        #
        #     bp = plt.boxplot(data, positions = [i, i+1], widths = 0.5, sym = '+')
        #     self.setBoxColors(bp)

        ax = plt.axes()
        #
        # keys = [""] + sorted(new_times.keys())
        #ax.set_xticklabels(set(x_ticks))
        #
        # m = 0
        # xticks = [0] + [t+m for t in range(1, len(keys) * 2 -1, 2)]
        ax.set_xticks(range(0, 1400, 64))
        #
        # # draw temporary red and blue lines and use them to create a legend
        # hB, = plt.plot([1, 1], color=self.old_matcher_colour)
        # hR, = plt.plot([1, 1], color=self.new_matcher_colour)
        # hMAX = plt.hlines(y=self.max_time, xmin = 0, xmax=len(keys) * 2, color = self.max_time_line, linestyles = 'dashed')
        # plt.legend((hB, hR, hMAX), ('Old Matcher', 'New Matcher', 'Cutoff Time'), bbox_to_anchor=(0.98, 0.15))
        # hB.set_visible(False)
        # hR.set_visible(False)


        plt.legend()
        plt.xlabel('Graph size')
        plt.ylabel('Time (s)')
        plt.yscale('log')
        # ml = MultipleLocator(2.5)
        # plt.axes().xaxis.set_minor_locator(ml)
        # plt.gca().xaxis.grid(True, which='minor')
        plt.title("Time for Matching")

        results_dir = "results/"
        plt.savefig(results_dir + "/abc_" + name + '.png', bbox_inches = 'tight', dpi = self.figure_dpi)
        plt.close()

        # print("Old failures")
        # for k, v in sorted(self.old_failures.items()):
        #     print("Size: {0} - Failures: {1}".format(k, v))
        #
        # print("New failures")
        # for k, v in sorted(self.new_failures.items()):
        #     print("Size: {0} - Failures: {1}".format(k, v))

    def parse_line(self, line):
        line = line.replace("[", "").replace("]", "")
        data = line.split(", ")

        if data == ['']: data = []

        data = [float(x) for x in data if x and x != 'None']
        return data

    def load_times_dir(self, times_dir):
        for times_file in sorted(os.listdir(times_dir)):
            #print("Loading: " + times_file)
            with open(times_dir + "/" + times_file) as f:
                old_times_str = f.readline().strip()
                new_times_str = f.readline().strip()
                first_decompose_str = f.readline().strip()
                second_decompose_str = f.readline().strip()

                old_times = self.parse_line(old_times_str)
                new_times = self.parse_line(new_times_str)
                first_decompose = self.parse_line(first_decompose_str)
                second_decompose = self.parse_line(second_decompose_str)

                first_failures = int(f.readline().strip())
                second_failures = int(f.readline().strip())

                if first_failures > 0:
                    print("Failure: First - " + times_file + " " + str(first_failures))
                if second_failures > 0:
                    print("Failure: Second - " + times_file + " " + str(second_failures))

                size = int(times_file.split("_")[2][1:].replace(".times",""))
                decompose_time = first_decompose + second_decompose

                self.decompose_times[size] += decompose_time

                s = times_file.split("_")
                graph_type = s[0]+s[1]

                self.decompose_times_types[graph_type][size] += decompose_time

                self.old_matching_times_types[graph_type][size] += old_times
                self.new_matching_times_types[graph_type][size] += new_times

                self.old_matching_times[size] += old_times
                self.new_matching_times[size] += new_times

                self.old_failures[size] += first_failures
                self.new_failures[size] += second_failures

                #self.plot_times(times_file, old_times, new_times)

    # function for setting the colors of the box plots pairs
    def setBoxColors(self, bp):
        plt.setp(bp['boxes'][0], color = self.old_matcher_colour)
        plt.setp(bp['caps'][0], color = self.old_matcher_colour)
        plt.setp(bp['caps'][1], color = self.old_matcher_colour)
        plt.setp(bp['whiskers'][0], color = self.old_matcher_colour)
        plt.setp(bp['whiskers'][1], color = self.old_matcher_colour)
        plt.setp(bp['fliers'][0], markeredgecolor = self.old_matcher_colour)
        plt.setp(bp['medians'][0], color = self.old_matcher_colour)

        plt.setp(bp['boxes'][1], color = self.new_matcher_colour)
        plt.setp(bp['caps'][2], color = self.new_matcher_colour)
        plt.setp(bp['caps'][3], color = self.new_matcher_colour)
        plt.setp(bp['whiskers'][2], color = self.new_matcher_colour)
        plt.setp(bp['whiskers'][3], color = self.new_matcher_colour)
        plt.setp(bp['fliers'][1], markeredgecolor = self.new_matcher_colour)
        plt.setp(bp['medians'][1], color = self.new_matcher_colour)


if __name__ == "__main__":

    times_dir = "./results/times/"
    plotter = Plotter()
    plotter.load_times_dir(times_dir)
    #plotter.plot_decompose_times()
    plotter.plot_matching_times(plotter.old_matching_times_types, plotter.new_matching_times_types, "")

    #for key in plotter.old_matching_times_types:
        #print(key)
     #   plotter.plot_matching_times(plotter.old_matching_times_types[key], plotter.new_matching_times_types[key], "_" + key)
