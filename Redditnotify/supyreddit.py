import reddit


r = reddit.Reddit(user_agent="Redditnotify")

def fetch_stories(subreddit, amount=5):
    stories = r.get_subreddit(subreddit).get_new(limit=5)
    return list(stories)

def submit(title, url):
    r.login('fixme', 'fixme')
    res = r.submit('fixme', url, title)
    return res


if __name__=='__main__':
    from pprint import pprint
    pprint (submit('Test', 'testurl'))
    #print fetch_stories('emmawatson')

