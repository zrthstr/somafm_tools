#!/usr/bin/env python3

#import os
import sys
import json
import tweepy
import requests
import argparse
import configparser
from bs4 import BeautifulSoup


CONFIG_FILE = "config"
CONFIG_SECTION = "DEFAULT"


def read_config_file():
    global consumer_key, consumer_secret, access_token, access_token_secret

    config_file = sys.path[0] + "/" + CONFIG_FILE
    config = configparser.ConfigParser() 
    config.read(config_file)

    consumer_key = config[CONFIG_SECTION]['consumer_key']
    consumer_secret = config[CONFIG_SECTION]['consumer_secret']
    access_token = config[CONFIG_SECTION]['access_token']
    access_token_secret = config[CONFIG_SECTION]['access_token_secret']


def get_song_info(nth):
    nth = 3
    ### nth is the minus_nth title counting downward
    ###    Played_At    Artist    Song    Album    ###
    station = 'cliqhop' ## this should be in config..
    url = "https://somafm.com/recent/%s.html" % station  # this too
    
    playtime_sel = "#playinc > table tr:nth-of-type(%d) td:nth-of-type(1)" %nth
    artist_sel = "#playinc > table tr:nth-of-type(%d) td:nth-of-type(2)" %nth
    song_sel = "#playinc > table tr:nth-of-type(%d) td:nth-of-type(3)" % nth
    album_sel = "#playinc > table tr:nth-of-type(%d) td:nth-of-type(4)" % nth
    
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    info=[soup.select(artist_sel)[0].getText(),
            soup.select(song_sel)[0].getText(),
            soup.select(album_sel)[0].getText()]
    
    song_info = json.dumps(info, ensure_ascii=False)
    
    return song_info


def count_saved_titles():
    count=len(api.user_timeline())
    print("[%d posts in list]" % count)
    return count


def list_saved_titles():
    posts = api.user_timeline()
    posts_text = [p.text for p in posts]
    for pt in posts_text:
        print(pt)


def save_title(song_n=0):
    print("song_n",song_n)
    song_info = get_song_info(3)
    print(song_info)
    api.update_status(song_info)
    sys.exit()
    pass


def list_played_titles():
    pass

def test_twitter():
    name = api.me().name
    print("ok. logged in as %s" % name)


def delete_last_title():
    count = count_saved_titles()
    post_text = api.user_timeline()[0].text
    post_id = api.user_timeline()[0].id
    api.destroy_status(post_id)
    new_count = count_saved_titles()
    if new_count + 1 == count:
        print("deleet post: %s with id:%d" %(post_text, post_id))
    else:
        print("failed to deleet post: %s with id:%d" %(post_text, post_id))



#def post_to_twitter(song_info):

def init_and_auth():
    global api
    read_config_file()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


def main():
    global api

    arg_parser = argparse.ArgumentParser()
    #arg_group = arg_parser.add_mutually_exclusive_group()
    arg_parser.add_argument("-t", "--test", action="store_true", help="test twitter auth with config")
    arg_parser.add_argument("-l", "--list", action="store_true", help="list all posts")
    arg_parser.add_argument("-c", "--count", action="store_true", help="count posts")
    arg_parser.add_argument("-s", "--save", action="count", help="save current song, -ss for previous song and so on")
#    arg_parser.add_argument("-p", "--past", action="store_true", help="list passt song")
    arg_parser.add_argument("-d", "--delete", action="store_true", help="delete last song") # should be count..
    args = arg_parser.parse_args()

    init_and_auth()

    if args.test:
        test_twitter()
    if args.list:
        list_saved_titles()
    if args.count:
        count_saved_titles()
    if args.delete:
        delete_last_title()
    if args.save:
        save_title(args.save)
#    if args.past:
#        list_past_titles()

    sys.exit()

if __name__ == '__main__' :
    main()

