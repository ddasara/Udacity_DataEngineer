import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

#log_data = config(['S3']['LOG_DATA'])
#song_data = config(['S3']['SONG_DATA']) 
#iam = config(['IAM_ROLE']['ARN'])
#log_json = config(['S3']['LOG_JSONPATH'])

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists dimsongplay"
user_table_drop = "drop table if exists dimuser"
song_table_drop = "drop table if exists dimsong"
artist_table_drop = "drop table if exists dimartist"
time_table_drop = "drop table if exists dimtime"

# CREATE TABLES

staging_events_table_create= (""" create table staging_events(artist varchar(200),
                                    auth varchar(200),
                                    firstName varchar(100),
                                    gender char,
                                    iteminsession int,
                                    lastName varchar(100),
                                    length float,
                                    level varchar(100),
                                    location varchar(300),
                                    method varchar,
                                    page varchar,
                                    registration varchar(300),
                                    sessionid int,
                                    song varchar(300),
                                    status int,
                                    ts bigint,
                                    userAgent varchar(500),
                                    userId int);
""")

staging_songs_table_create = (""" create table staging_songs(num_songs int,
                                    artist_id varchar(300),
                                    artist_latitude float,
                                    artist_logitude float,
                                    artist_location varchar(300),
                                    artist_name varchar(200),
                                    song_id varchar(100),
                                    title varchar(200),
                                    duration float,
                                    year int);
""")

songplay_table_create = (""" create table dimsongplay(
                            songplay_id int identity(1,1) Primary Key sortkey distkey,
                            start_time timestamp NOT NULL ,
                            userId int NOT NULL,
                            level varchar(100),
                            song_id varchar(100) NOT NULL,
                            artist_id varchar(300) NOT NULL,
                            session_id int,
                            location varchar(300),
                            user_agent varchar(500));
""")

user_table_create = (""" create table dimuser(userId int Primary Key sortkey ,
                        first_name varchar(100) NOT NULL, 
                        last_name varchar(100) NOT NULL, 
                        gender varchar(10) NOT NULL,
                        level varchar(100) NOT NULL);
""")

song_table_create = (""" create table dimsong(song_id text Primary Key sortkey,
                        title varchar(300) NOT NULL,
                        artist_id varchar(300) NOT NULL,
                        year int NOT NULL,
                        duration float);
""")

artist_table_create = ("""create table dimartist(artist_id text Primary Key sortkey,
                        name varchar(100) NOT NULL,
                        location varchar(300),
                        latitude float, 
                        longitude float);
""")

time_table_create = (""" create table dimtime(start_time timestamp Primary Key sortkey distkey,
                        hour int NOT NULL,
                        day text NOT NULL,
                        week int NOT NULL,
                        month text NOT NULL, 
                        year int NOT NULL, 
                        weekday text NOT NULL);
""")

# STAGING TABLES

staging_events_copy = (""" COPY staging_events FROM {}
                           iam_role {}
                           format as json{};
""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'] ,config['S3']['LOG_JSONPATH'])

staging_songs_copy = (""" COPY staging_songs FROM {}
                           iam_role {}
                           format as json 'auto';
""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = (""" insert into dimsongplay(start_time, userId, level,song_id,session_id,location,user_agent)
                        select DISTINCT staging_events.ts as start_time,
                        staging_events.userId as userId,
                        staging_events.level as level, 
                        staging_songs.song_id as song_id,
                        staging_events.session_d as session_id,
                        staging_events.location as location,
                        staging_events.userAgent as user_agent
                        from staging_events 
                        join staging_songs on staging_songs.title = staging_events.title and 
                        staging_events.artist = staging_songs.artist_name and staging_events.page = 'Nextsong';
""")

user_table_insert = (""" insert into dimuser (userId, first_name, last_name, gender, level) 
                        select DISTINCT staging_events.userId as userId ,
                        staging_events.firstName as first_name,
                        staging_events.lastName as last_name, 
                        staging_events.gender as gender,
                        staging_events.level as level
                        from staging_events where staging_events.userId is not null and page = 'NextSong';
""")

song_table_insert = (""" insert into dimsong(song_id, title, artist_id, year, duration)
                        select DISTINCT staging_songs.song_id as song_id, 
                        staging_songs.title as title, 
                        staging_songs.artist_id as artist_id,
                        staging_songs.year as year, 
                        staging_songs.duration as duration
                        from staging_songs 
                        join staging_events on staging_events = staging_songswhere staging_songs.song_id is not null and ; 
""")

artist_table_insert = (""" insert into dimartist(artist_id,name, location,latitude,longitude)
                            select DISTINCT staging_songs.artist_id as artist_id,
                            staging_songs.artist_name as name,
                            staging_songs.artist_location as location,
                            staging_songs.artist_latitude as latitude,
                            staging_songs.artist_longitude as longitude from staging_songs
                            where staging_songs.artist_id is not null;
""")

time_table_insert = (""" insert into dimtime(start_time, hour, day, week, month, year, weekday)
                            select DISTINCT start_time, 
                            extract(hour from start_time),
                            extract(day from start_time),
                            extract(week from start_time),
                            extract(month from start_time),
                            extract(year from start_time),
                            extract(weekday from start_time) from dimsongplay;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
