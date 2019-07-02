import psycopg2
import uuid
from configparser import ConfigParser

#this program will pull from the server at any given time to produce data to resample the mindmap

#sql server info
connection = psycopg2.connect(client_id=parser.get('reddit_raw', 'client_id'), client_secret=parser.get('reddit_raw', 'client_secret'), user_agent='my user agent')
class Submission(object):
    def __init__(self, title, subreddit):
        self.title = title
        self.subreddit = subreddit

titles = []
words = []

#this function connects to SQL server and pulls data to be used for the mindmap
def sql_select():
    cursor = connection.cursor()
    print('Connected!')

    #this tells the SQL server to only select the title column
    sql_select_command = """SELECT title, subreddit FROM reddit_info"""
    cursor.execute(sql_select_command)
    sub_titles = cursor.fetchall()
    print('SQL pull complete')
    for row in sub_titles:
        titles.append(Submission(title, subreddit))

def split_words(list):
    #this splits the list into individual words
    newlist = [word for line in list for word in line.split()]
    words.extend(newlist)

def most_common(list):
    return max(set(list), key=list.count)

#this call sql_select to pull form the SQL server and print out the title results
sql_select()
connection.close()
print(len(titles))
split_words(titles)
print(len(words))
print(most_common(words))
#print(write_list_to_file)
print("SQL Connection Closed")


