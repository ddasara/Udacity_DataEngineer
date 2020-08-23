# DROP TABLES

songplay = " drop table songplay"
users = "drop table users"
songs = "drop table songs"
artists = "drop table artists"
time = "drop table time"

# CREATE TABLES

songplay = (""" create table if not exists songplay (songplay_id SERIAL PRIMARY KEY NOT NULL,\
start_time varchar , userId int, level varchar, song_id varchar, artist_id varchar, sessionId int,\
location varchar, userAgent varchar )""")

users = (""" create table if not exists users (userId int PRIMARY KEY NOT NULL, first_name varchar,last_name varchar,gender varchar,\
level varchar)""")

songs = (""" create table if not exists songs(song_id varchar NOT NULL PRIMARY KEY, title varchar, \
artist_id varchar NOT NULL, year varchar, duration numeric)""")

artists = (""" create table if not exists artists(artist_id varchar PRIMARY KEY NOT NULL, artist_name varchar,\
location varchar, latitude numeric, longitude numeric)""")

time = (""" create table if not exists time(start_time varchar PRIMARY KEY NOT NULL, hour int, day int, month int,\
year int, weekday int, week int)""")
 
# INSERT RECORDS

songplay_table_insert = (""" insert into songplay(songplay_id, start_time, userId, level, song_id, artist_id, sessionId,\
location, userAgent) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (songplay_id) DO NOTHING""")

user_table_insert = (""" insert into users (userId, first_name, last_name, gender, level) values(%s, %s,%s,%s,%s)\
on conflict (userId) do update set level = excluded.level""")

song_table_insert = (""" insert into songs (song_id, title, artist_id, year, duration) values(%s, %s, %s, %s, %s)\
ON CONFLICT (song_id) DO NOTHING""")

artist_table_insert = (""" insert into artists (artist_id, artist_name, location, latitude, longitude)\
values(%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING""")


time_table_insert = (""" insert into time(start_time,  hour, day,  month, year, weekday,week) \
values(%s,%s, %s,%s,%s,%s,%s) ON CONFLICT (start_time) DO NOTHING""")

# FIND SONGS

song_select = (""" select songs.song_id, songs.artist_id from artists join songs on songs.artist_id = artists.artist_id \
and songs.title = %s and artists.artist_name = %s and songs.duration = %s""")

# QUERY LISTS

create_table_queries = [songplay, users, songs, artists, time]
drop_table_queries = [songplay, users, songs, artists, time]