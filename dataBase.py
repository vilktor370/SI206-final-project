import sqlite3
from api import *


def set_up_data_base(file_name):
    conn = sqlite3.connect(file_name)

    cur = conn.cursor()
    return cur, conn


def create_table(cur, conn):
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Artist (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, artist TEXT)")
    print("Artist table successfully created!")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Genre (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT)")
    print("Genre table successfully created!")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Track (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT, price, INTEGER, artist_id INTEGER, genre_id INTEGER)")
    print("Track table successfully created!")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS LastFM (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, listeners, INTEGER, mbid TEXT, url TEXT, artist_id INTEGER)")
    print("Track LastFM successfully created!")
    conn.commit()


def add_data_to_artist(cur, conn):
    song_dict = top_100_songs_from_billboard()
    cur.execute("SELECT MAX(id) FROM Artist")
    id = cur.fetchone()[0]
    if id == None:
        count = 0
    else:
        count = id + 1
    artist_list = list(song_dict.values())
    while True:
        if count >= len(artist_list):
            break
        cur.execute("SELECT name FROM LastFM WHERE name = (?)", (artist_list[count],))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO Artist (id,artist) VALUES (?,?)",
                        (count, artist_list[count]))
            count += 1
        if count % 25 == 0:
            break
    conn.commit()

def add_data_to_genre_track(cur, conn):
    song_dict = top_100_songs_from_billboard()
    my_dict = {}
    genre_set = set()
    for song in list(song_dict.keys()):
        for each_song in get_songs_from_itunes(song):
            if each_song['kind'] == 'song':
                title = each_song.get("trackName")
                price = float(each_song.get("trackPrice", 0))
                my_dict[title] = price
                genre = each_song.get('primaryGenreName')
                genre_set.add(genre)
                break
    cur.execute("SELECT MAX(id) FROM Genre")
    id = cur.fetchone()[0]
    if id == None:
        count = 0
    else:
        count = id + 1
    for i in genre_set:
        if count >= len(genre_set):
            break
        cur.execute("SELECT name FROM Genre WHERE name = (?)", (i,))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO Genre (id,name) VALUES (?,?)",
                        (count, i))
            count += 1
        if count % 25 == 0:
            break

    cur.execute("SELECT MAX(id) FROM Track")
    id = cur.fetchone()[0]
    if id == None:
        count = 0
    else:
        count = id + 1
    track_tuple = list(my_dict.items())
    while True:
        if count >= len(track_tuple):
            break
        cur.execute("SELECT title FROM Track WHERE title = (?)", (track_tuple[count][0],))
        if cur.fetchone() == None:
            cur.execute(
                "INSERT INTO Track (id, title, price, artist_id, genre_id) VALUES (?,?,?,?,?)",
                (count, track_tuple[count][0], track_tuple[count][1], count, count))
            count += 1
        if count % 25 == 0:
            break
    conn.commit()


def add_data_to_LastFM(cur, conn):
    song_dict = top_100_songs_from_billboard()
    artist_list = []
    listeners_list = []
    mbid_list = []
    url_list = []
    for artist in list(song_dict.keys()):
        for each_item in get_song_from_last_fm(artist):
            if each_item['name'] == artist:
                artist_name = each_item['name']
                listeners = int(each_item['listeners'])
                mbid = each_item.get('mbid', "No Id")
                url = each_item['url']
                artist_list.append(artist_name)
                listeners_list.append(listeners)
                mbid_list.append(mbid)
                url_list.append(url)
    cur.execute("SELECT MAX(id) FROM LastFM")
    id = cur.fetchone()[0]
    if id == None:
        count = 0
    else:
        count = id + 1
    while True:
        if count >= len(artist_list):
            break
        cur.execute("SELECT name FROM LastFM WHERE name = (?)", (artist_list[count],))
        if cur.fetchone() == None:
            cur.execute(
                "INSERT INTO LastFM (id, name, listeners, mbid, url,artist_id ) VALUES (?,?,?,?,?,?)",
                (count, artist_list[count], listeners_list[count], mbid_list[count],
                 url_list[count], count))
            count += 1
        if count % 25 == 0:
            break
    conn.commit()
