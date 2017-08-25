import numpy as np
import matplotlib.pyplot as plt



def plot_times(times):

    for key in times.keys():

        print(key)
        #data = np.array((times[key]['old'], times[key]['new']))
        #data = np.rot90(data)

        labels = ['Old','New']
        fs = 10  # fontsize
        plt.figure()
        #data = np.random.lognormal(size = (37, 4), mean = 1.5, sigma = 1.75)

        #fig = plt.boxplot(data, showmeans=True, meanline=True)
        #fig.set_title('Times', fontsize = fs)

        #plt.plot(data['old'], range(100), data['new'], range(100))
        t = np.arange(0., 5., 0.2)

        # red dashes, blue squares and green triangles
        plt.plot(range(100), times[key]['old'], 'r*', range(100), times[key]['new'], 'bs',)

        plt.show()