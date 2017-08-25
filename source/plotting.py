import numpy as np
import matplotlib.pyplot as plt



def plot_times(times):

    labels = ['Old']
    fs = 10  # fontsize
    plt.figure()
    fig = plt.boxplot(times['iso_m2D_s16']["old"], labels=labels, showmeans=True, meanline=True)
    #fig.set_title('Times', fontsize = fs)

    plt.show()