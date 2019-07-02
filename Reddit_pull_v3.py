import praw
import psycopg2
from datetime import datetime
import uuid
from configparser import ConfigParser

# userid and passwords
parser = ConfigParser()
parser.read('dev.ini')

# reddit api praw info
reddit = praw.Reddit(client_id=parser.get('reddit_raw', 'client_id'), client_secret=parser.get('reddit_raw', 'client_secret'), user_agent='my user agent')

# objects for sorting data to index
class Front(object):
    def __init__(self, subreddit, submission_id, time_created, rank, time, subscribers):
        self.subreddit = subreddit
        self.submission_id = submission_id
        self.time_created = time_created
        self.rank = rank
        self.time = time
        self.subscribers = subscribers

class Submission(object):
    def __init__(self, submission_id, author_id, score, numb_comments, title, words, uuid):
        self.submission_id = submission_id
        self.author_id = author_id
        self.score = score
        self.numb_comments = numb_comments
        self.title = title
        self.words = words
        self.uid = uuid.uuid1()

class Author(object):
    def __init__(self, name, author_id, comment_karma, link_karma, submission_id):
        self.name = name
        self.author_id = author_id
        self.comment_karma = comment_karma
        self.link_karma = link_karma
        self.submission_id = submission_id

front_info = []
submission_info = []
author_info = []

def front_pull():
    print('Reddit front')
    rank = 0
    for submission in reddit.subreddit('all').hot(limit=25):
        rank +=1
        subreddit = str(submission.subreddit)
        submission_id = submission.subreddit.id
        time_created = submission.subreddit.created_utc
        subscribers = int(submission.subreddit.subscribers)
        time = datetime.today()
        front_info.append(Front(subreddit, submission_id, time_created, rank, time, subscribers))

def submission_pull():
    print('Reddit submission')
    for submission in reddit.subreddit('all').hot(limit=25):
        submission_id = submission.id
        author_id = submission.author.id
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 200 else title
        title = str(title)
        words = title.replace(' ', ',')
        submission_info.append(Submission(submission_id, author_id, score, numb_comments, title, words, uuid))


def author_pull():
    print('Reddit author')
    for submission in reddit.subreddit('all').hot(limit=25):
        name = submission.author.name
        author_id = submission.author.id
        comment_karma = submission.author.comment_karma
        link_karma = submission.author.link_karma
        submission_id = submission.id
        author_info.append(Author(name, author_id, comment_karma, link_karma, submission_id))
