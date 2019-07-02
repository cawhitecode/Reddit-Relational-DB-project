import praw
import psycopg2
import time
from datetime import datetime
import uuid
from configparser import ConfigParser

# Userid and passwords
parser = ConfigParser()
parser.read('dev.ini')

# reddit api praw connection info
reddit = praw.Reddit(client_id=parser.get('reddit_raw', 'client_id'), client_secret=parser.get('reddit_raw', 'client_secret'), user_agent='my user agent')

# object to index the reddit info and to recall later for SQL translation
class Subreddit(object):
    def __init__(self, title, time):
        self.title = title
        self.time = time
        self.uid = uuid.uuid1()

# stores objects for indexing
mind_info = []

# using reddit API praw to make an object or submission and indexing them
def reddit_mind_pull():
    for submission in reddit.subreddit('all').hot(limit=30):
        bad_title = str(submission.title)
        title = bad_title.replace("'", "%")
        title = (title[:200] + '..') if len(title) > 200 else title
        title = title.replace(" ", ",")
        time = datetime.today()
        mind_info.append(Subreddit(title, time))

# this connects to the Postgres SQL server and puts the object info into a readable formart for sql
def sql_mind_inject():
     # postgresql database connection info
    connection = psycopg2.connect(user = parser.get('psy_connect', 'user'), password = parser.get('psy_connect', 'password'), host = parser.get('psy_connect', 'host'),
    port = parser.get('psy_connect', 'port'), database = "postgres")
    cursor = connection.cursor()

    #this is where the magic happens for SQL convert. 0 = obj.tite, 1 = obj.time, 2 = obj.uid.hex, uid is based off time and a unique key generated
    for obj in mind_info:
        format_sql  = """INSERT INTO reddit_mind (title, time, uuid_key)
        VALUES ('{0}', '{1}', '{2}');"""
        cursor.execute(format_sql.format(obj.title, obj.time, obj.uid.hex))

    connection.commit()

# function used to consolidate all other functions per reddit_bot_mind
def reddit_mind_all():
    reddit_mind_pull()
    sql_mind_inject()
    mind_info.clear()

# calls the function for all
reddit_mind_all()
