# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id INT PRIMARY KEY NOT NULL,
                                                                  start_time BIGINT,
                                                                  userId int NOT NULL,
                                                                  level VARCHAR,
                                                                  song_id VARCHAR,
                                                                  artist_id VARCHAR,
                                                                  sessionId INT,
                                                                  location VARCHAR,
                                                                  userAgent VARCHAR);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (userId INT PRIMARY KEY NOT NULL,
                                                          firstName VARCHAR,
                                                          lastName VARCHAR,
                                                          gender CHAR(1),
                                                          level VARCHAR);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id VARCHAR PRIMARY KEY NOT NULL,
                                                          title VARCHAR,
                                                          artist_id VARCHAR,
                                                          year INT,
                                                          duration FLOAT);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR NOT NULL,
                                                              artist_name VARCHAR,
                                                              artist_location VARCHAR,
                                                              artist_latitude FLOAT,
                                                              artist_longitude FLOAT)
""")


time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP NOT NULL, 
                                                        hour INT, 
                                                        day INT, 
                                                        week INT, 
                                                        month INT, 
                                                        year INT, 
                                                        weekday INT)
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (songplay_id, start_time, userId, level, song_id, artist_id, sessionId, location, userAgent)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (songplay_id) DO NOTHING;
""")

user_table_insert = ("""INSERT INTO users (userId, firstName, lastName, gender, level)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (userID) DO UPDATE SET level = EXCLUDED.level;
""")


song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, artist_name , artist_location, artist_latitude, artist_longitude)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
""")                                                              


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT a.song_id, a.artist_id
                  FROM songs as a
                  JOIN artists as b ON a.artist_id = b.artist_id
                  WHERE title = %s
                  AND artist_name = %s
                  AND duration = %s
                  ;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]