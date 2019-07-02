import psycopg2
from configparser import ConfigParser

# parser used for userid and passwords
parser = ConfigParser()
parser.read('dev.ini')

# using configParser for connection info and password
connection = psycopg2.connect(user = parser.get('psy_connect', 'user'), password = parser.get('psy_connect', 'password'), host = parser.get('psy_connect', 'host'),
port = parser.get('psy_connect', 'port'), database = "postgres")

def sql_front_table():
    # postgresql database connection info see above
    cursor = connection.cursor()

    # this creates the front table in SQL
    sql_command = """
    CREATE TABLE reddit_front_info (
    subreddit VARCHAR(225),
    submissionID VARCHAR(225),
    timeCreated VARCHAR(225),
    rank INTEGER,
    time VARCHAR(225) PRIMARY KEY,
    subscribers INTEGER);"""
    cursor.execute(sql_command)
    connection.commit()
    print('Front Table created')

def sql_submission_table():
    # postgresql database connection info
    cursor = connection.cursor()

    # this creates the submission table in SQL
    sql_command = """
    CREATE TABLE reddit_submission_info (
    submissionID VARCHAR(225),
    authorID VARCHAR(225),
    upvotes INTEGER,
    comments INTEGER,
    title VARCHAR(225),
    words VARCHAR(500),
    uid VARCHAR(225));"""
    cursor.execute(sql_command)
    connection.commit()
    print('Submission Table created')


def sql_author_table():
    # postgresql database connection info
    cursor = connection.cursor()

    # this creates the author table in SQL
    sql_command = """
    CREATE TABLE reddit_author_info (
    name VARCHAR(225),
    authorID VARCHAR(225),
    commentKarma INTEGER,
    linkKarma INTEGER,
    submissionID VARCHAR(225));"""
    cursor.execute(sql_command)
    connection.commit()
    print('Author Table created')

def sql_drop_reddit_tables():
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE  reddit_front_info;""")
    cursor.execute("""DROP TABLE  reddit_submission_info;""")
    cursor.execute("""DROP TABLE  reddit_author_info;""")
    connection.commit()
    print('Front, submission, and author tables dropped')

def sql_connection_close():
    connection.close()

