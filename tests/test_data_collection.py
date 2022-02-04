from src.util import get_reddit_connection


import praw

def test_connection():
    reddit = get_reddit_connection()
    assert isinstance(reddit, praw.reddit.Reddit)
