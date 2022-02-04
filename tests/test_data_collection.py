import praw
from src.util import *


def test_connection():
    reddit = get_reddit_connection()
    assert isinstance(reddit, praw.reddit.Reddit)


def test_get_post():
    reddit = get_reddit_connection()
    post_id = "d6xoro"
    post = get_post(reddit, post_id)
    assert isinstance(post, praw.reddit.Submission)
