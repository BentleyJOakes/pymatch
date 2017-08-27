import numpy as np
import matplotlib.pyplot as plt

import os

def plot_times(times_file, old_times, new_times):

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

def load_times_dir(times_dir):
    for times_file in sorted(os.listdir(times_dir)):
        with open(times_dir + "/" + times_file) as f:
            old_times_str = f.readline().strip()
            new_times_str = f.readline().strip()

            old_times_str = old_times_str.replace("[", "").replace("]", "")
            old_times = old_times_str.split(", ")
            old_times = list(map(float, old_times))

            new_times_str = new_times_str.replace("[", "").replace("]", "")
            new_times = new_times_str.split(", ")
            new_times = list(map(float, new_times))

            plot_times(times_file, old_times, new_times)

if __name__ == "__main__":

    times_dir = "./results/times/"
    load_times_dir(times_dir)
