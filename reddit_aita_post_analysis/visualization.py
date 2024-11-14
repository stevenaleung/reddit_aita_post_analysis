import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_tlc_analysis_figure(summary, num_hours_cutoff):
    hours_since_post_creation = summary["hours_since_post_creation"]
    scores = summary["scores"]
    nta = summary["nta"]
    yta = summary["yta"]
    info = summary["info"]
    other = summary["other"]

    fig_handle = plt.figure()
    plt.scatter(
        hours_since_post_creation[np.where(nta)],
        scores[np.where(nta)],
        c="tab:green",
        label="NTA",
    )
    plt.scatter(
        hours_since_post_creation[np.where(yta)],
        scores[np.where(yta)],
        c="tab:orange",
        label="YTA",
    )
    plt.scatter(
        hours_since_post_creation[np.where(info)],
        scores[np.where(info)],
        c="tab:purple",
        label="INFO",
    )
    plt.scatter(
        hours_since_post_creation[np.where(other)],
        scores[np.where(other)],
        c="tab:blue",
        label="Other",
    )
    plt.xlim((0, num_hours_cutoff))
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
    plt.scatter(nta_idxs + 1, scores[nta_idxs], c="tab:green", label="NTA")
    plt.scatter(yta_idxs + 1, scores[yta_idxs], c="tab:orange", label="YTA")
    plt.scatter(info_idxs + 1, scores[info_idxs], c="tab:purple", label="INFO")
    plt.scatter(other_idxs + 1, scores[other_idxs], c="tab:blue", label="Other")
    plt.xlim((0, num_comments))
    plt.grid("on")
    plt.xlabel("Comments ranked by 'best'")
    plt.ylabel("Voting score")
    plt.title("Sentiment of 'best' ranked top level comments")
    plt.legend()
    plt.xticks(range(1, num_comments, 2))
    return fig_handle


def create_total_score_figure(post_df: pd.DataFrame, num_tlc: int) -> mpl.figure.Figure:
    """Create a number of bar charts that tally the score of every comment in the
    comment tree. The user can specify the number of comments to analyze"""
    df_grouped = post_df.groupby(["tlc_idx", "judgement"]).sum()

    fig_handle = plt.figure()
    # adjust the layout of the figure depending on the number of top level comments
    # specified. by default, the figure will add columns before it adds rows
    num_cols = int(np.ceil(np.sqrt(num_tlc)))
    num_rows = int(np.ceil(num_tlc / num_cols))

    for tlc_idx in range(num_tlc):
        comment_scores_summed = df_grouped.loc[tlc_idx]["comment_score"]
        plt.subplot(num_rows, num_cols, tlc_idx + 1)
        create_total_score_plot(comment_scores_summed)

    fig_handle.autofmt_xdate()
    plt.tight_layout()
    return fig_handle


def create_total_score_plot(comment_scores_summed: pd.Series) -> None:
    # when performing a groupby, the values in the pandas series index are not sorted.
    # they are ordered is by first occurrence instead. we'd like to assign certain
    # colors to certain judgements, so we need the order to be consistent
    judgement_scores = {"NTA": 0, "YTA": 0, "UNCLEAR": 0, "INFO": 0}
    for judgement in comment_scores_summed.index:
        judgement_scores[judgement] = comment_scores_summed.loc[judgement]

    bar_colors = ["tab:green", "tab:orange", "tab:blue", "tab:purple"]

    plt.bar(judgement_scores.keys(), judgement_scores.values(), color=bar_colors)
    plt.ylabel("Voting score")


def create_score_per_depth_figure(
    post_df: pd.DataFrame, num_tlc: int
) -> mpl.figure.Figure:
    """
    Create a number of score per depth figures. The user can specify the number of
    comments to analyze
    """
    df_grouped = post_df.groupby(["tlc_idx", "comment_depth", "judgement"]).sum()

    fig_handle = plt.figure()
    # adjust the layout of the figure depending on the number of top level comments
    # specified. by default, the figure will add columns before it adds rows
    num_cols = int(np.ceil(np.sqrt(num_tlc)))
    num_rows = int(np.ceil(num_tlc / num_cols))

    for tlc_idx in range(num_tlc):
        comment_scores_summed = df_grouped.loc[tlc_idx]["comment_score"]
        ax_handle = plt.subplot(num_rows, num_cols, tlc_idx + 1)
        create_score_per_depth_plot(comment_scores_summed, ax_handle)

    plt.tight_layout()
    return fig_handle


def create_score_per_depth_plot(comment_scores_summed: pd.DataFrame, ax_handle) -> None:
    """
    Create a series of bar charts that tally the judgement scores at each comment depth
    """
    pivoted_df = (
        comment_scores_summed.reset_index()
        .groupby(["comment_depth", "judgement"])["comment_score"]
        .aggregate("first")
        .unstack()
    )

    bar_colors = {
        "NTA": "tab:green",
        "YTA": "tab:orange",
        "UNCLEAR": "tab:blue",
        "INFO": "tab:purple",
    }

    missing_cols = set(bar_colors.keys()).difference(set(pivoted_df.columns))
    pivoted_df[list(missing_cols)] = np.NaN
    pivoted_df = pivoted_df[bar_colors.keys()]

    pivoted_df.plot.barh(color=bar_colors.values(), ax=ax_handle)
    plt.gca().invert_yaxis()
    plt.ylabel("Comment depth")
    plt.gca().get_legend().remove()
