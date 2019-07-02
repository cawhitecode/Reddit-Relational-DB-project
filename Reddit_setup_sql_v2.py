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

# object for submissions to index after this
class Subreddit(object):
    def __init__(self, title, subreddit, score, numb_comments, subscribers, rank, time, uuid):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.numb_comments = numb_comments
        self.subscribers = subscribers
        self.rank = rank
        self.time = time
        self.uid = uuid.uuid1()


# stores objects for indexing
subreddit_info = []

# using reddit API praw to make an object or submission and indexing them
def reddit_pull():
    print('Reddit')
    rank = 0
    for submission in reddit.subreddit('all').hot(limit=25):
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


# test to make sure objects are working
def test_data():
    for obj in subreddit_info:
        print("Title:", obj.title)
        print("/r", obj.subreddit)
        print("Score:", obj.score)
        print("Comments:", obj.numb_comments)
        print("Subscribers:",obj.subscribers)
        print(obj.uid.hex)
        print("-----------")

# this connects to the server and put the reddit info into a readable formart for sql
def sql_inject():
    # postgresql database connection info
    connection = psycopg2.connect(user = parser.get('psy_connect', 'user'), password = parser.get('psy_connect', 'password'), host = parser.get('psy_connect', 'host'),
    port = parser.get('psy_connect', 'port'), database = "postgres")
    cursor = connection.cursor()
    print('Connected!')

    # comment out to avoid dropping table
    # cursor.execute("""DROP TABLE reddit_info_time_rank;""")

    # this creates the table in SQL
    sql_command = """
    CREATE TABLE reddit_info_time_rank (
    title VARCHAR(225),
    subreddit VARCHAR(225),
    upvotes INTEGER,
    comments INTEGER,
    subscribers INTEGER,
    time VARCHAR(225) PRIMARY KEY,
    rank INTEGER,
    uid  VARCHAR(225));"""

    cursor.execute(sql_command)

     # this is where the magic happens for SQL convert. 0 = obj.tite, 1 = obj.subreddit, 2 = obj.score, uid is based off time and a unique key generated
    for obj in subreddit_info:
        format_sql  = """INSERT INTO reddit_info_time_rank (title, subreddit, upvotes, comments, subscribers, time, rank, uid)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');"""
        cursor.execute(format_sql.format(obj.title, obj.subreddit, obj.score, obj.numb_comments, obj.subscribers, obj.time, obj.rank, obj.uid.hex))

        connection.commit()

    connection.close()
    print("----SUCCESS----")

# function that calls all functions
def reddit_setup_all():
    reddit_pull()
    test_data()
    sql_inject()
    print('injection done')
    subreddit_info.clear()
    print('cleared subreddit_info')

# calls function reddit_setup_all to execute all functions
reddit_setup_all()
