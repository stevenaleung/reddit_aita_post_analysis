# reddit_aita_post_analysis

A package to analyze posts from reddit.com/r/AmItheAsshole/

## Quick start

```python
import src.util as util
import src.visualization as vis

post_id = "123456"

reddit = util.get_reddit_connection()
post = util.get_post(reddit, post_id)
summary = util.analyze_post_tlc(post)

num_hours_cutoff = 12
fig = vis.create_tlc_analysis_figure(summary, num_hours_cutoff)
plt.show()

num_comments = 20
fig = vis.create_tlc_ranking_figure(summary, num_comments)
plt.show()
```