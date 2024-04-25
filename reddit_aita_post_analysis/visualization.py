import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def create_tlc_analysis_figure(summary, num_hours_cutoff):
    hours_since_post_creation = summary["hours_since_post_creation"]
    scores = summary["scores"]
    nta = summary["nta"]
    yta = summary["yta"]
    info = summary["info"]
    other = summary["other"]

    fig_handle = plt.figure()
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
    return fig_handle


def create_tlc_ranking_figure(summary, num_comments):
    scores = summary["scores"][1:num_comments]
    nta = summary["nta"][1:num_comments]
    yta = summary["yta"][1:num_comments]
    info = summary["info"][1:num_comments]
    other = summary["other"][1:num_comments]

    nta_idxs = np.where(nta)[0]
    yta_idxs = np.where(yta)[0]
    info_idxs = np.where(info)[0]
    other_idxs = np.where(other)[0]

    fig_handle = plt.figure()
    plt.scatter(nta_idxs+1, scores[nta_idxs], c="tab:green", label="NTA")
    plt.scatter(yta_idxs+1, scores[yta_idxs], c="tab:orange", label="YTA")
    plt.scatter(info_idxs+1, scores[info_idxs], c="tab:purple", label="INFO")
    plt.scatter(other_idxs+1, scores[other_idxs], c="tab:blue", label="Other")
    plt.xlim((0,num_comments))
    plt.grid("on")
    plt.xlabel("Comments ranked by 'best'")
    plt.ylabel("Voting score")
    plt.title("Sentiment of 'best' ranked top level comments")
    plt.legend()
    plt.xticks(range(1,num_comments,2))
    return fig_handle
