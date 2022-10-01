import matplotlib.pyplot as plt
from const import CONST
import numpy as np
import pandas as pd
import data_mgr as dmgr

colors_set = np.array(["orange","purple","beige","brown","gray","cyan","magenta","red","green","blue","yellow","pink"])

####################################################################################################################
# Create MATPLOTLIB Graphs of Data Given np matrix
def plt_histogram_by_key(numpy_matrix, bins=50):
    for idx, k in enumerate(CONST.KEYLIST):
        plt.hist(numpy_matrix[:][idx], snap=True, bins=bins)
        plt.gca().set(title=k, ylabel="Frequency")
        plt.show()


####################################################################################################################
# Create MATPLOTLIB Graph of one key vs another
def plt_key_by_key(keylist: tuple, numpy_matrix):
    rows, cols = np.shape(numpy_matrix)

    x_idx = CONST.KEYLIST.index(keylist[0])
    y_idx = CONST.KEYLIST.index(keylist[1])

    x = np.array(numpy_matrix[:][x_idx])
    y = np.array(numpy_matrix[:][y_idx])

    plt.scatter(x, y, s=5)
    plt.gca().set(xlabel=keylist[0], ylabel=keylist[1])
    plt.show()

def plt_all(x, y, z_list, idx=0):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    idx_f = len(z_list) 


    if idx_f == idx:
        plt.show()
        return 1

    ax.scatter(x, y, z_list[idx], cmap='inferno')
    plt.title(CONST.KEYLIST[idx])
    plt.xlabel("Key (X)")
    plt.ylabel("Tempo (Y)")
    plt.savefig("data/img3d/" + CONST.KEYLIST[idx])
    plt_all(x, y, z_list, idx=idx+1)


def plt_all_norm(x_all, idx=0):
    if idx == len(CONST.KEYLIST):
        return 0

    fig = plt.figure()
    ax = fig.add_subplot()
    
    x = x_all[idx]
    x = np.sort(x)
    mu = np.median(x)
    sigma = np.std(x)
    y = dmgr.prob_density(x, mu, sigma)
    ax.plot(x, y)
    plt.title(CONST.KEYLIST[idx])
    idx+=1
    plt_all_norm(x_all, idx)
    plt.show()
