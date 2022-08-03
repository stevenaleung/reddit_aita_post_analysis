import praw
import numpy as np
import csv


def analyze_post_tlc(post_id):
    # get the list of top level comments
    reddit = get_reddit_connection()
    post = get_post(reddit, post_id)
    tlc_list = get_top_level_comments(post)

    # comment creation times
    post_creation_time = get_post_creation_time(post)
    tlc_creation_times = get_comment_creation_time(tlc_list)
    tlc_seconds_since_post_creation = tlc_creation_times - post_creation_time
    tlc_hours_since_post_creation = convert_seconds_to_hours(tlc_seconds_since_post_creation)
    
    # voting score
    tlc_scores = get_comment_scores(tlc_list)

    # combine all data
    summary = get_judgement_counts(tlc_list)
    summary["hours_since_post_creation"] = tlc_hours_since_post_creation
    summary["scores"] = tlc_scores
    return summary


def get_reddit_connection():
    return praw.Reddit("bot1", user_agent="N/A")


def get_post(reddit, post_id):
    return reddit.submission(id=post_id)


def get_top_level_comments(post):
    tlc_list = []
    for tlc in post.comments:
        tlc_list.append(tlc)
    return tlc_list


def get_post_creation_time(post):
    return post.created_utc


def get_comment_creation_time(comment_list):
    num_comments = len(comment_list)
    comment_creation_times = np.zeros(num_comments)
    for idx, comment in enumerate(comment_list):
        comment_creation_times[idx] = comment.created_utc
    return comment_creation_times


def convert_seconds_to_hours(seconds):
    return seconds / 3600


def get_comment_scores(comment_list):
    num_comments = len(comment_list)
    comment_scores = np.zeros(num_comments)
    for idx, comment in enumerate(comment_list):
        comment_scores[idx] = comment.score
    return comment_scores


def get_judgement_counts(comment_list):
    num_comments = len(comment_list)
    nta = np.full((num_comments,), False)
    yta = np.full((num_comments,), False)
    info = np.full((num_comments,), False)
    for idx, tlc in enumerate(comment_list):
        nta[idx] = tlc.body.find("NTA") >= 0
        yta[idx] = tlc.body.find("YTA") >= 0
        info[idx] = tlc.body.find("INFO") >= 0
    other = np.invert(yta) & np.invert(nta) & np.invert(info)
    judgement_counts = {"nta": nta,
                        "yta": yta,
                        "info": info,
                        "other": other}
    return judgement_counts


def save_post_to_csv(post_id, csv_filename):
    reddit = get_reddit_connection()
    post = get_post(reddit, post_id)
    tlc_list = get_top_level_comments(post)

    comment_stack = []
    comment_level = 0
    for tlc in reversed(tlc_list):
        comment_stack.append((comment_level, tlc))

    depth_first_write_to_csv(csv_filename, comment_stack)

    return None


def depth_first_write_to_csv(csv_filename, comment_stack):
    csv_handle = open(csv_filename, "w")
    csv_writer = csv.writer(csv_handle)

    while comment_stack:
        comment_level, comment = comment_stack.pop()
        row = create_row(comment, comment_level)
        csv_writer.writerow(row)
        for child_comment in reversed(comment.replies):
            comment_stack.append((comment_level+1, child_comment))

    csv_handle.close()

    return None


def create_row(comment, comment_level):
    row = [""] * comment_level
    row.append(get_author_name(comment))
    return row


def get_author_name(comment):
    if comment.author is None:
        author_name = "[deleted]"
    else:
        author_name = comment.author.name
    return author_name
