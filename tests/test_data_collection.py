import praw
import reddit_aita_post_analysis.util as util


def test_connection():
    reddit = util.get_reddit_connection()
    assert isinstance(reddit, praw.reddit.Reddit)


def test_get_post():
    reddit = util.get_reddit_connection()
    post_id = "d6xoro"
    post = util.get_post(reddit, post_id)
    assert isinstance(post, praw.reddit.Submission)
