#!/bin/python3
from requests import get
from sys import argv

# get spotify api key and spotify playlist id
if len(argv) >= 3:
    print('Found arguments, using them.')
    api_key = argv[1]
    playlist_id = argv[2]
else:
    api_key = input('Input your Spotify API key: ')

    if not api_key:
        print('No api key specified')
        exit(1)

    playlist_id = input('Input the playlist id: ')

    if not playlist_id:
        print('No playlist id specified')
        exit(2)

# ask spotify api for the playlist details
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# gets the playlist name and each track's most important information
fields='name%2Ctracks.items(added_at%2Ctrack(album(name%2Crelease_date)%2Cartists(name%2Ctype)%2Cname))'

r = get(f'https://api.spotify.com/v1/playlists/{playlist_id}?fields={fields}', headers=headers)

details = r.text

# show the user; save to file
print(details)
with open(f'spotify-playlist-{playlist_id}.json', 'w') as f:
    print(details, file=f)
print('Done! Spotify playlist details written to file.')

