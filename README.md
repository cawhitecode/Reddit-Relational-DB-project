# Chris White
# Reddit-Relational-DB-project

If you're looking for a how to setup. I'll include a short how to underneath the summary "How to"</br>
</br>
This project is used to practice Python and SQL together.</br>
The purpose of this project was to get a better understandment of Reddit and what controls their engagement. The hypothesis that the amount of comments per a submission drives the upvote counter higher, thus to the front page. I was also curious on which titles or words were most often on each subreddit on the /r/all.</br>
</br>
## Reasoning:
</br>
The question comes up, I have this cool idea and want to spread this idea far and wide. Which subreddit do I choose? Which wording do I go with and which do I avoid? Do you want to focus on the most comment engagment to drive conversation or do you just want some time to shine on the front page of reddit? Maybe a mix of all of the above? With the right data we can give answers to all these...
</br>
The intial answer well answer together is what drivers most upvotes? Is it the amount of comments, maybe subreddit, or subscribers? Most likely a mix of all three, but I went we with a hypothesis that comments drives the amount of upvotes higher. Thus what's the ratio of upvotes and comments per each subreddit? We will need a few bits of data:</br>
</br>
1. The title</br>
2. Subreddit</br>
3. Number of Upvotes</br>
4. Number of Comments</br>
5. Number of Subscribers</br>
6. The rank of the submission</br>
</br>
Note: Version 3 has expanded this to submission ID, time created, time of the pull, words of the title, name of the author, author ID, author's comment and link karma, used in relational database to save space and time for later use and analysis
</br>
### Current result:
1. My hypothesis that comments do drive engagment was shown by correlation to upvotes of .289899, however subscribers to the particular subreddit had a higher correlation than comments at .313972. However to have a valid conclusion we'll have to wait a little bit for the a bigger sample size on the wording question as well. 
</br>
</br>
# How to:

Use Reddit API to gather information then use it gage engagement</br>
You'll need:</br>
PuTTy - https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html</br>
PGadmin4 </br>
Reddit API account/PRAW</br>
psycopg2</br>
BlockingScheduler(if you want data to pull at set times)</br>
</br>
I'm using a PostgreSQL database, but if you want to use another SQL just change out psycopg2 for the corresponding library import. </br>
</br>
How to install/use - Windows </br>
1. Setup a server - I used DigitalOcean.com - the server does have to support the database language you choose(SQL)</br>
2. Install PuTTy - type in your host name/address = I.P. address of server, port 22</br>
3. When logged in on Ubuntu type "adduser *yourname*" without quotes then "usermod -aG sudo *yourname*" **yourname is whatever you want it to be**</br>
4. command list:</br>
*python3*</br>
sudo apt-get update</br>
sudo apt-get install mc</br>
sudo apt-get -y install python3-pip</br>
sudo apt-get -y install python3-dev</br>
sudo -H pip3 install --upgrade pip</br>
sudo apt-get install postgresql postgresql-contrib  **note this changes if you want to a different use a different SQL language**</br>
sudo -i -u postgres</br>
CREATE USER **yourname** WITH PASSWORD **'yourpassword'**</br>
sudo -i -u root</br>
5. Open PGadmin4 using **yourname** as User name and **yourpassword** as password</br>
keep in mind that your server may not be listening to your program.</br>
6. Don't forget to install PRAW, Psycopg2, and BlockingScheduler</br>
7. Open and save both files. Reddit.py is the initial setup for making the table and pulling the data. Reddit_pull.py pulls the data continously</br>
