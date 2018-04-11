import spotipy
import queue
import spotipy.util as util
from time import sleep
import pandas as pd #Dataframe, Series
import numpy as np

import io
import sys, getopt

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import networkx as nx
import os

sp = spotipy.Spotify()
q = queue.Queue()
scope = 'playlist-modify-private playlist-modify-public playlist-read-private user-library-read'
userid = input("What is your spotify username/user id? ")
playlistid = input("What is the ID of the playlist you would like to put the tracks into? ")

os.environ['SPOTIPY_CLIENT_ID'] = "17f99cb7fd3547d3beb06012a5864442"
os.environ['SPOTIPY_CLIENT_SECRET'] = "3d7ef5e132e64a129673fa58ddf3c6bc"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:8888"
token = util.prompt_for_user_token(userid, scope, client_id="17f99cb7fd3547d3beb06012a5864442", client_secret="3d7ef5e132e64a129673fa58ddf3c6bc")

spotify = spotipy.Spotify(auth=token)
artist_names = []
results = spotify.current_user_saved_tracks()
for item in results["items"]:
        track = item["track"]
        artist_names.append(track["artists"][0]["name"])

while results["next"]:
    for item in results["items"]:
        track = item["track"]
        artist_names.append(track["artists"][0]["name"])
    results = spotify.next(results)

setOfArtists = set(artist_names)

newReleases = spotify.new_releases("AU")

songsToCheckOut = []

aritstsInNewReleases = []

while newReleases["albums"]["next"]:
    for release in newReleases["albums"]["items"]:
        if(release["album_type"] == "album"):
            album = spotify.album(release["id"])
            i = 0
            for track in album["tracks"]["items"]:
                weLikeArtist = False
                for artist in release["artists"]:
                    aritstsInNewReleases.append(artist["name"])
                    if artist["name"] in setOfArtists:
                        weLikeArtist = True
                        break

                if weLikeArtist:
                    songsToCheckOut.append(track)



        if(release["album_type"] == "single"):
            for artist in release["artists"]:
                aritstsInNewReleases.append(artist["name"])
                weLikeArtist = False
                if artist["name"] in setOfArtists:
                    weLikeArtist = True
                    break

                if weLikeArtist:
                    songsToCheckOut.append(track)
    newReleases = spotify.next(newReleases["albums"])
for track in songsToCheckOut:
    spotify.user_playlist_add_tracks(userid,playlistid, [track["id"]])
len(songsToCheckOut)
