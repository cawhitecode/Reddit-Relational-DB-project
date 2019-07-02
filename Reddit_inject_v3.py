
import psycopg2
from configparser import ConfigParser
from Reddit_pull_v3 import front_info
from Reddit_pull_v3 import submission_info
from Reddit_pull_v3 import author_info

parser = ConfigParser()
parser.read('dev.ini')

# SQL connection info
connection = psycopg2.connect(user = parser.get('psy_connect', 'user'), password = parser.get('psy_connect', 'password'), host = parser.get('psy_connect', 'host'),
port = parser.get('psy_connect', 'port'), database = "postgres")

# this connects to the server and put the reddit info into a readable formart for sql
def sql_inject_front():
    cursor = connection.cursor()

    # this is where the magic happens for SQL convert. 0 = obj.subreddit, 1 = obj.submission_id, 2 = obj.time_created, uid is based off time and a unique key generated
    for obj in front_info:
        format_sql  = """INSERT INTO reddit_front_info (subreddit, submissionID, timeCreated, rank, time, subscribers)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"""
        cursor.execute(format_sql.format(obj.subreddit, obj.submission_id, obj.time_created, obj.rank, obj.time, obj.subscribers))

        connection.commit()

def sql_inject_submission():
    cursor = connection.cursor()

    # this is where the magic happens for SQL convert. 0 = obj.subreddit, 1 = obj.submission_id, 2 = obj.time_created, uid is based off time and a unique key generated
    for obj in submission_info:
        format_sql  = """INSERT INTO reddit_submission_info (submissionid, authorid, upvotes, comments, title, words, uid)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');"""
        cursor.execute(format_sql.format(obj.submission_id, obj.author_id, obj.score, obj.numb_comments, obj.title, obj.words, obj.uid.hex))

        connection.commit()

def sql_inject_author():
    cursor = connection.cursor()

    # this is where the magic happens for SQL convert. 0 = obj.subreddit, 1 = obj.submission_id, 2 = obj.time_created, uid is based off time and a unique key generated
    for obj in author_info:
        format_sql  = """INSERT INTO reddit_author_info (name, authorid, commentkarma, linkkarma, submissionid)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');"""
        cursor.execute(format_sql.format(obj.name, obj.author_id, obj.comment_karma, obj.link_karma, obj.submission_id))

        connection.commit()

def sql_connection_close():
    connection.close()

