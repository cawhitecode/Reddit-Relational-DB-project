
import os
import Reddit_pull_v3
import Reddit_inject_v3
import Reddit_sql_table_setup_v3 as table_setup
from datetime import datetime
import schedule
import time
import pytz

front_info = []
submission_info = []
author_info = []

def reddit_pull():
        Reddit_pull_v3.front_pull()
        Reddit_pull_v3.submission_pull()
        Reddit_pull_v3.author_pull()
        print('Pulls Complete')

def reddit_inject():
        Reddit_inject_v3.sql_inject_front()
        Reddit_inject_v3.sql_inject_submission()
        Reddit_inject_v3.sql_inject_author()
        Reddit_inject_v3.sql_connection_close()
        print('Inject Complete')

def reddit_clear():
        front_info.clear()
        submission_info.clear()
        author_info.clear()
        print('Front, Submissions, and Authors cleared')

def reddit_all():
        reddit_pull()
        reddit_inject()
        reddit_clear()
        timeus = datetime.now(pytz.utc).astimezone(pytz.timezone('US/Central'))
        print('Reddit all Done: ', timeus)

schedule.every(2).hours.do(reddit_all)


while 1:
    schedule.run_pending()
    time.sleep(1)
