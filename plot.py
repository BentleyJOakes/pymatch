import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os

class Plotter:

    def __init__(self):
        self.decompose_times = defaultdict(list)

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
        plt.title("Times for: " + name)
        #plt.show()

        results_dir = "results/"
        plt.savefig(results_dir + "/" + name + '.png', bbox_inches = 'tight')
        plt.close()





    def plot_decompose_times(self):
        name = "decompose_times"
        labels = sorted(self.decompose_times.keys())
        plt.figure()
        data = [list(self.decompose_times[k]) for k in sorted(self.decompose_times.keys())]
        plt.boxplot(data, labels = labels, showmeans = True, meanline = True)
        plt.xlabel('Graph size')
        plt.ylabel('Time (s)')
        plt.title("Time for Decomposing During Matching")
        results_dir = "results/"
        plt.savefig(results_dir + "/" + name + '.png', bbox_inches = 'tight')
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

                self.plot_times(times_file, old_times, new_times)



if __name__ == "__main__":

    times_dir = "./results/times/"
    plotter = Plotter()
    plotter.load_times_dir(times_dir)
    plotter.plot_decompose_times()
