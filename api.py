import json, requests

import time
from bs4 import BeautifulSoup


def get_songs_from_itunes(song_name):
    r = requests.get("https://itunes.apple.com/search?", params={
        'term': song_name,
        'media': 'music'
    })
    time.sleep(4)
    print("Pausing a little bit..")
    data = json.loads(r.text)
    return data['results']


def get_artists_info(artist):
    r = requests.get("https://itunes.apple.com/search?", params={
        'term': artist,
    })
    time.sleep(4)
    print("Pausing a little bit..")
    data = json.loads(r.text)
    return data['results']


def get_song_from_last_fm(artist):
    api_key = "2336b4bfc71d6c5b5bcc18864b12228b"
    shared_secret = "99d30b8efcc4c7a2eea1158d281616a3"
    base_url = "http://ws.audioscrobbler.com/2.0/"
    r = requests.get(base_url, params={
        'method': "artist.search",
        "artist": artist,
        "api_key": api_key,
        'format': 'json'
    })
    data = json.loads(r.text)
    return data['results']['artistmatches']['artist']


# get data from billboard
# return a dictionary with top 100 songs {song's name: artist}
def top_100_songs_from_billboard():
    r = requests.get("https://www.billboard.com/charts/hot-100")
    soup = BeautifulSoup(r.content, "html.parser")
    song_info = soup.find_all('span', {
        'class': "chart-element__information"})
    song_dict = {}
    for song in song_info:
        song_name = song.find("span", {
            'class': "chart-element__information__song text--truncate color--primary"}).text
        song_artist = song.find("span", {
            'class': "chart-element__information__artist text--truncate color--secondary"}).text
        song_dict[song_name] = song_artist
    return song_dict
