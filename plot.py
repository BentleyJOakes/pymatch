import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from collections import defaultdict
import os

class Plotter:

    def __init__(self):
        self.decompose_times = defaultdict(list)
        self.old_matching_times = defaultdict(list)
        self.new_matching_times = defaultdict(list)

        self.old_matcher_colour = '#dd2233'
        self.old_matcher_colour2 = "0.75"

        self.new_matcher_colour = "#2233dd"
        self.new_matcher_colour2 = "1.00"

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
        labels = sorted(self.decompose_times.keys())
        fig = plt.figure()
        fig.set_size_inches(self.figure_size_x, self.figure_size_y)
        data = [list(self.decompose_times[k]) for k in sorted(self.decompose_times.keys())]
        plt.boxplot(data, labels = labels, showmeans = True, meanline = True, sym = '+')
        plt.xlabel('Graph size')
        plt.ylabel('Time (s)')
        plt.title("Time for Decomposing During Matching")
        results_dir = "results/"
        plt.savefig(results_dir + "/abc_" + name + '.png', bbox_inches = 'tight', dpi = self.figure_dpi)
        plt.close()

    def plot_matching_times(self):
        print("Creating matching time graph...")
        name = "matching_times"

        fig = plt.figure()
        fig.set_size_inches(self.figure_size_x, self.figure_size_y)
        i = 0.5
        for k in sorted(self.new_matching_times.keys()):
            data = [self.old_matching_times[k], self.new_matching_times[k]]

            dividing_line = i+1.5
            plt.axvline(dividing_line, ls = "-", color = "0.75")

            bp = plt.boxplot(data, positions = [i, i+1], widths = 0.5, sym = '+')
            self.setBoxColors(bp)
            i+=2
        # labels = []
        # for key in sorted(self.new_matching_times.keys()):
        #     labels.append("Old-" + str(key))
        #     labels.append("New-" + str(key))
        #
        #
        #
        # data = []
        # for k in sorted(self.old_matching_times.keys()):
        #     data.append(self.old_matching_times[k])
        #     data.append(self.new_matching_times[k])
        #
        # plt.boxplot(data, labels = labels, showmeans = True, meanline = True)
        ax = plt.axes()

        keys = [""] + sorted(self.new_matching_times.keys())
        ax.set_xticklabels(keys)

        m = 0
        xticks = [0] + [t+m for t in range(1, len(keys) * 2 -1, 2)]
        ax.set_xticks(xticks)

        # draw temporary red and blue lines and use them to create a legend
        hB, = plt.plot([1, 1], color=self.old_matcher_colour)
        hR, = plt.plot([1, 1], color=self.new_matcher_colour)
        hMAX = plt.hlines(y=300, xmin = 0, xmax=len(keys) * 2, color = self.max_time_line, linestyles = 'dashed')
        plt.legend((hB, hR, hMAX), ('Old Matcher', 'New Matcher', 'Cutoff Time'), bbox_to_anchor=(0.98, 0.15))
        hB.set_visible(False)
        hR.set_visible(False)

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

    def parse_line(self, line):
        line = line.replace("[", "").replace("]", "")
        data = line.split(", ")

        if data == ['']: data = []

        data = list(map(float, data))
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

                size = int(times_file.split("_")[2][1:].replace(".times",""))
                decompose_time = first_decompose + second_decompose

                self.decompose_times[size] += decompose_time

                self.old_matching_times[size] += old_times
                self.new_matching_times[size] += new_times

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
    plotter.plot_decompose_times()
    plotter.plot_matching_times()
