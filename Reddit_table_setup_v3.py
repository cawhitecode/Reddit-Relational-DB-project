import os
import Reddit_sql_table_setup_v3 as table_setup

# use to reset tables, don't uncomment unless you want to delete tables
#table_setup.sql_drop_reddit_tables()

table_setup.sql_front_table()
table_setup.sql_submission_table()
table_setup.sql_author_table()
table_setup.sql_connection_close()
