A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. 

We have to create database for Sparkify and perform ETL process to load the data.

It has two datasets. 1. Songs dataset
		     2. Log dataset

Fact table:
songplay - which contains (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) as fields

Dimension Tables:
1. Users : user_id, first_name, last_name, gender, level
2. Songs : song_id, title, artist_id, year, duration
3. Artists : artist_id, name, location, latitude, longitude
4. Time : start_time, hour, day, week, month, year, weekday


sql_queries.py -> contains all sql queries
create_tables.py -> drops and creates tables.
etl.ipynb -> reads and processes a single file from song_data and log_data and loads the data into tables
etl.py reads and processes files from song_data and log_data and loads them into tables
test.ipynb -> displays the first few rows of each table to let you check your database


First run create_tables.py to make sure to create fact and dimesion tables.
Create ETL tasks in the etl.ipyn file
Next run etl.py to run the whole etl process to load the data into our facts and dimesion tables