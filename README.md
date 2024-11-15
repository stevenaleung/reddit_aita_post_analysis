# reddit_aita_post_analysis

[![Build Status](https://github.com/stevenaleung/reddit_aita_post_analysis/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/stevenaleung/reddit_aita_post_analysis/actions/workflows/ci.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/stevenaleung/reddit_aita_post_analysis/branch/main/graph/badge.svg?token=36E0JH5GYV)](https://codecov.io/gh/stevenaleung/reddit_aita_post_analysis)


A package to analyze posts from reddit.com/r/AmItheAsshole/

## Quick start

```python
import reddit_aita_post_analysis.util as util
import reddit_aita_post_analysis.visualization as vis
import matplotlib.pyplot as plt

post_id = "123456"

reddit = util.get_reddit_connection()
post = util.get_post(reddit, post_id)

summary = util.analyze_post_tlc(post)
post_df = util.to_dataframe(post)
```

Create scatter plots to show top level judgements 
```python
num_hours_cutoff = 12
fig = vis.create_tlc_analysis_figure(summary, num_hours_cutoff)
plt.show()

num_comments = 20
fig = vis.create_tlc_ranking_figure(summary, num_comments)
plt.show()
```

Create bar charts to show total judgement scores
```python
num_comments = 9
fig = vis.create_total_score_figure(post_df, num_comments)
plt.show()
```
