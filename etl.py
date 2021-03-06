import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Function to process the songs JSON files into songs and artists dimension tables
    - Opens the song file
    - Selects the fields required for the songs table and inserts the song record
    - Selects the fields required for the artists table and inserts the artists record
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[:,['song_id','title','artist_id','year','duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.loc[:,['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Function to process the log file JSON into time and users dimension and tables and creates the songplay fact table
    - Opens the log file
    - Filters to only records relevant to song plays
    - Converts the start time to a TIMESTAMP and extracts the hour, day, week, month, year and weekday.  Inserts into the time dimension table
    - Selects the fields required for the users dimension table and inserts the records
    - Gets the artist_id and song_id from the songs and artists table for the record in the log file
    - Extracts all other required fields for the songplay fact table and inserts the record
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_df = pd.concat([t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday], axis = 1)
    time_df.columns = ['start_time','hour','day', 'week', 'month', 'year', 'weekday']

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:,['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates().reset_index(drop=True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        # insert songplay record
        songplay_data = (index, row.ts, row.userId, row.level, song_id, artist_id, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Function to process the log and song files by executing the process_song_file and process_log_file functions
    - Scans the directory for song and log files, prints the number of files found to a log
    - Processes either the song or log file by executing the relevant function
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Runs the process_data function to process either song data or log data
    """
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()