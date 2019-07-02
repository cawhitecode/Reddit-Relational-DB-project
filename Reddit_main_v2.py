import os
import schedule
import time
from datetime import datetime
import time
import pytz

# Runs every two hours, the programs - reddit_bot_mind and reddit_pull.py
def hour_tasks_2():
    os.system('python3 reddit_bot_mind_v2.py')
    print('Reddit bot Done')
    os.system('python3 reddit_pull_v2.py')
    timeus = datetime.now(pytz.utc).astimezone(pytz.timezone('US/Central'))
    print('Reddit Main Done: ', timeus)

#calls the function hour_tasks_2 and timer is set for 2 hours. Seconds and minutes also available
schedule.every(2).hours.do(hour_tasks_2)

while 1:
    schedule.run_pending()
    time.sleep(1)