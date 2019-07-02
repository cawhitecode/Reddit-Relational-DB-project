
import praw
import psycopg2
import schedule
import time
from datetime import datetime
import uuid
from configparser import ConfigParser

# Userid and passwords
parser = ConfigParser()
parser.read('dev.ini')

# Reddit api praw info
reddit = praw.Reddit(client_id=parser.get('reddit_raw', 'client_id'), client_secret=parser.get('reddit_raw', 'client_secret'), user_agent='my user agent')

# Object to index the subreddit info and to recall later for SQL translation
class Subreddit(object):
    def __init__(self, title, subreddit, score, numb_comments, subscribers, rank, time, uid):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.numb_comments = numb_comments
        self.subscribers = subscribers
        self.rank = rank
        self.time = time
        self.uid = uuid.uuid1()

# Stores objects for indexing later
subreddit_info = []

# Using reddit API to make an object or submission and indexing them
def reddit_pull():
    rank = 0
    for submission in reddit.subreddit('all').hot(limit=30):
        rank +=1
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 200 else title
        subreddit = str(submission.subreddit)
        score = int(submission.score)
        numb_comments = int(submission.num_comments)
        subscribers = int(submission.subreddit.subscribers)
        time = datetime.today()
        subreddit_info.append(Subreddit(title, subreddit, score, numb_comments, subscribers, rank, time, uuid))

# This connects to the server and put the reddit info into a readable formart for sql
def sql_inject():
    connection = psycopg2.connect(user = parser.get('psy_connect', 'user'), password = parser.get('psy_connect', 'password'), host = parser.get('psy_connect', 'host'),
    port = parser.get('psy_connect', 'port'), database = "postgres")
    cursor = connection.cursor()

    # this is where the magic happens for SQL convert. 0 = obj.tite, 1 = obj.subreddit, 2 = obj.score, uid is based off time and a unique key generated
    for obj in subreddit_info:
        format_sql  = """INSERT INTO reddit_info_time_rank (title, subreddit, upvotes, comments, subscribers, time, rank, uid)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');"""
        cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers, obj.time, obj.rank, obj.uid.hex))

    connection.commit()
    connection.close()

# Used to run program while giving a few clarifications to make sure program is working as intended for test
def reddit_all():
    reddit_pull()
    sql_inject()
    subreddit_info.clear()
    
# uns the reddit_all function that runs the whole program
reddit_all()