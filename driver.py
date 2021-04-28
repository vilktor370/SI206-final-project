from dataBase import *
from api import *
import csv


def download_database():
    cur, conn = set_up_data_base('test.db')
    create_table(cur, conn)
    # add_data_to_LastFM(cur, conn)
    add_data_to_artist(cur, conn)
    # add_data_to_genre_track(cur, conn)


def get_data():
    cur, conn = set_up_data_base("test.db")
    cur.execute("SELECT * FROM Artist")
    rows = cur.fetchall()
    artist_list = [row[1] for row in rows]

    cur.execute(
        "SELECT Track.title, Track.price  FROM Track JOIN Artist ON Track.genre_id = Artist.id")
    rows = cur.fetchall()
    track_list = [row[0] for row in rows]
    price_list = [row[1] for row in rows]

    cur.execute("SELECT Genre.name FROM Genre JOIN Artist ON Genre.id = Artist.id")
    rows = cur.fetchall()
    genre_list = [row[0] for row in rows]

    cur.execute("SELECT LastFM.listeners, LastFM.url FROM LastFM")
    rows = cur.fetchall()
    listeners = [row[0] for row in rows]
    url = [row[1] for row in rows]

    return artist_list, track_list, genre_list, price_list, listeners, url


def write_csv():
    artist_list, track_list, genre_list, price_list, listeners, url = get_data()
    with open('songs.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['id',
                             'artist', 'song_name', 'price'])
        for i in range(len(artist_list)):
            csv_writer.writerow(
                [i + 1, artist_list[i], track_list[i], '$' + str(price_list[i])])


download_database()
# write_csv()
