#!/usr/bin/env python3

import json
import tweepy
import requests
import configparser
from bs4 import BeautifulSoup


CONFIG_FILE = "config"
CONFIG_SECTION = "DEFAULT"


def read_config_file():
    global consumer_key, consumer_secret, access_token, access_token_secret

    config = configparser.ConfigParser() 
    config.read(CONFIG_FILE)

    consumer_key = config[CONFIG_SECTION]['consumer_key']
    consumer_secret = config[CONFIG_SECTION]['consumer_secret']
    access_token = config[CONFIG_SECTION]['access_token']
    access_token_secret = config[CONFIG_SECTION]['access_token_secret']


def get_song_info():
    ###    Played_At    Artist    Song    Album    ###
    station = 'cliqhop'
    url = "https://somafm.com/recent/%s.html" % station
    
    playtime_sel = "#playinc > table tr:nth-of-type(3) td:nth-of-type(1)"
    artist_sel = "#playinc > table tr:nth-of-type(3) td:nth-of-type(2)"
    song_sel = "#playinc > table tr:nth-of-type(3) td:nth-of-type(3)"
    album_sel = "#playinc > table tr:nth-of-type(3) td:nth-of-type(4)"
    
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    info=[soup.select(artist_sel)[0].getText(),
            soup.select(song_sel)[0].getText(),
            soup.select(album_sel)[0].getText()]
    
    song_info = json.dumps(info, ensure_ascii=False)
    
    return song_info


def post_to_twitter(song_info):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(song_info)


if __name__ == '__main__' :
    read_config_file()
    song_info = get_song_info()
    post_to_twitter(song_info)

