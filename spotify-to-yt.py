#!/bin/python3
from ytmusicapi import YTMusic
import json
from sys import argv
from fuzzywuzzy import fuzz
from youtube_dl import YoutubeDL

# TODO: make this look better

def collect_artists(artist_list, name_key='name'):
    return ', '.join(map(lambda x: x[name_key], artist_list))

def shorten_str(s, length=15):
    return (s[:length - 2] + '..') if len(s) > length else s

def print_song(name, artists, album_name, index=None, vid_id=None, score=None):
    if index:
        print(f'{index:2}: ', end='')
    print(f'"{shorten_str(name):^15}" by "{shorten_str(artists, 20):^20}" from "{shorten_str(album_name):^15}" ', end='')
    if vid_id:
        print(f'[{vid_id}] ', end='')
    if score:
        print(f'{{{score:3}}}', end='')
    print()

def spotify_to_yt(filename):
    # load spotify playlist details from file
    with open(filename, 'r') as f:
        details = json.load(f)

    ytmusic = YTMusic()
    song_file = open('song_ids.txt', 'w')
    video_ids = []

    print('Playlist Name:', details['name'])
    for track in details['tracks']['items']:
        album = track['track']['album'] # name, release_date
        album_name = album['name']
        artists = track['track']['artists'] # [] name, type
        artists_str = collect_artists(artists)
        name = track['track']['name']

        search_query = f'{name} {artists[0]["name"]}'
        yt_songs = ytmusic.search(search_query, filter='songs')

        distances = []
        i = 1

        print(' 0: NONE OF THEM')
        print_song(name, artists_str, album_name, index='EX')
        for song in yt_songs:
            s_name = song['title']
            s_artists = collect_artists(song["artists"])
            s_album_name = song.get('album', {'name': 'N/A'})['name']

            # compute fuzz ratio between song title, artist, and album
            song_dist = fuzz.token_sort_ratio(name, s_name)
            artist_dist = fuzz.partial_token_sort_ratio(artists_str, s_artists)
            album_dist = fuzz.partial_token_sort_ratio(album_name, s_album_name)

            # higher = better
            score = song_dist * 4 + artist_dist * 2 + album_dist
            distances.append((score, i))

            print_song(s_name, s_artists, s_album_name, i, song['videoId'], score)
            i += 1

        # get close matches
        print('Closest matches:')
        best_match = 0
        for score, index in reversed(sorted(filter(lambda x: x[0] >= 500, distances))):
            # hacky way to get best match
            if best_match == 0:
                best_match = index

            song = yt_songs[index - 1]
            s_name = song['title']
            s_artists = collect_artists(song['artists'])
            s_album_name = song.get('album', {'name': 'N/A'})['name']
            print_song(s_name, s_artists, s_album_name, index, song['videoId'], score)

        choice = input(f'Which song is the correct one (default: {best_match})? ')
        choice = best_match if not choice else int(choice)

        if choice < 0:
            print('Got negative number, quitting.')
            break
        elif choice > 0 and choice < len(yt_songs):
            video_id = yt_songs[choice - 1]['videoId']
        else:
            print('Using YTDL fallback...')
            with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
                try:
                    info = ydl.extract_info(f'ytsearch:{search_query}', download=False)
                    if not info:
                        raise Exception()
                    video = info['entries'][0]
                    video_id = f'video["id"] (?)'
                    print_song(video['title'], video['uploader'], 'N/A', vid_id=video_id)
                except:
                    video_id = None
                    print('Could not find song.')
            # video_id = input('Input the video id of the song (default: skip): ')

        if video_id:
            video_ids.append(video_id)
        print(f'"{name}" by "{artists_str}": {video_id}', file=song_file)
        print()

    # remove the "(?)" from some of the video ids
    flat_vid_ids = list(map(lambda x: x.split()[0], video_ids))

    print(f'www.youtube.com/watch_videos?video_ids={",".join(flat_vid_ids)}')
    song_file.close()

if __name__ == '__main__':
    spotify_to_yt(argv[1])

