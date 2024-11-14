import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_top_level_score_vs_time_figure(
    post_df: pd.DataFrame, num_hours_cutoff: float
) -> mpl.figure.Figure:
    is_within_time_cutoff = post_df["hours_since_post_creation"] < num_hours_cutoff
    is_top_level_comment = post_df["comment_depth"] == 0
    subset_df = post_df.loc[is_within_time_cutoff & is_top_level_comment]

    color_dict = {
        "NTA": "tab:green",
        "YTA": "tab:orange",
        "UNCLEAR": "tab:blue",
        "INFO": "tab:purple",
    }

    fig_handle = plt.figure()
    for judgement, color in color_dict.items():
        ax_df = subset_df[subset_df["judgement"] == judgement]
        plt.scatter(
            ax_df["hours_since_post_creation"],
            ax_df["comment_score"],
            c=color,
            label=judgement,
        )

    plt.xlim((0, num_hours_cutoff))
    plt.grid("on")
    plt.xlabel("Time since original post (hr)")
    plt.ylabel("Voting score")
    plt.title("Sentiment of top level comments")
    plt.legend()
    return fig_handle


def create_top_level_score_vs_ranking_figure(
    post_df: pd.DataFrame, num_comments: int
) -> mpl.figure.Figure:
    is_top_level_comment = post_df["comment_depth"] == 0
    subset_df = post_df.loc[is_top_level_comment][:num_comments]

    color_dict = {
        "NTA": "tab:green",
        "YTA": "tab:orange",
        "UNCLEAR": "tab:blue",
        "INFO": "tab:purple",
    }

    fig_handle = plt.figure()
    for judgement, color in color_dict.items():
        ax_df = subset_df[subset_df["judgement"] == judgement]
        plt.scatter(
            ax_df["tlc_idx"] + 1,
            ax_df["comment_score"],
            c=color,
            label=judgement,
        )

    plt.xlim((0, num_comments))
    plt.grid("on")
    plt.xlabel("Comments ranked by 'best'")
    plt.ylabel("Voting score")
    plt.title("Sentiment of 'best' ranked top level comments")
    plt.legend()
    plt.xticks(range(1, num_comments, 2))
    return fig_handle


def create_total_score_figure(comments_df: pd.DataFrame) -> mpl.figure.Figure:
    """Create a number of bar charts that tally the score of every comment in the
    comment tree. The user can specify the number of comments to analyze"""
    grouped_df = comments_df.groupby(["tlc_idx", "judgement"]).sum()
    tlc_idxs = pd.unique(grouped_df.index.get_level_values(0))
    num_tlc = len(tlc_idxs)

    fig_handle = plt.figure()
    # adjust the layout of the figure depending on the number of top level comments
    # specified. by default, the figure will add columns before it adds rows
    num_cols = int(np.ceil(np.sqrt(num_tlc)))
    num_rows = int(np.ceil(num_tlc / num_cols))

    for idx, tlc_idx in enumerate(tlc_idxs):
        comment_scores_summed = grouped_df.loc[tlc_idx]["comment_score"]
        plt.subplot(num_rows, num_cols, idx + 1)
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


def create_score_per_depth_figure(comments_df: pd.DataFrame) -> mpl.figure.Figure:
    """
    Create a number of score per depth figures. The user can specify the number of
    comments to analyze
    """
    grouped_df = comments_df.groupby(["tlc_idx", "comment_depth", "judgement"]).sum()
    tlc_idxs = pd.unique(grouped_df.index.get_level_values(0))
    num_tlc = len(tlc_idxs)

    fig_handle = plt.figure()
    # adjust the layout of the figure depending on the number of top level comments
    # specified. by default, the figure will add columns before it adds rows
    num_cols = int(np.ceil(np.sqrt(num_tlc)))
    num_rows = int(np.ceil(num_tlc / num_cols))

    for idx, tlc_idx in enumerate(tlc_idxs):
        comment_scores_summed = grouped_df.loc[tlc_idx]["comment_score"]
        ax_handle = plt.subplot(num_rows, num_cols, idx + 1)
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
