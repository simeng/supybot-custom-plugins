import reddit

r = reddit.Reddit(user_agent="Redditnotify")

def fetch_stories(subreddit, amount=5):
    stories = r.get_subreddit(subreddit).get_new(limit=5)
    return list(stories)


if __name__=='__main__':
    print fetch_stories('emmawatson')

