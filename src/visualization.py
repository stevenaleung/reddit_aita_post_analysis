import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_results(summary, num_hours_cutoff):
    hours_since_post_creation = summary["hours_since_post_creation"]
    scores = summary["scores"]
    nta = summary["nta"]
    yta = summary["yta"]
    info = summary["info"]
    other = summary["other"]

    plt.scatter(hours_since_post_creation[np.where(nta)], scores[np.where(nta)], c="tab:green", label="NTA")
    plt.scatter(hours_since_post_creation[np.where(yta)], scores[np.where(yta)], c="tab:orange", label="YTA")
    plt.scatter(hours_since_post_creation[np.where(info)], scores[np.where(info)], c="tab:purple", label="INFO")
    plt.scatter(hours_since_post_creation[np.where(other)], scores[np.where(other)], c="tab:blue", label="Other")
    plt.xlim((0,num_hours_cutoff))
    plt.grid("on")
    plt.xlabel("Time since original post (hr)")
    plt.ylabel("Voting score")
    plt.title("Sentiment of top level comments")
    plt.legend()
    plt.show()
