# Random Scripts

### Spotify to YouTube flow
#### Step 0: Setup
Install `youtube-dl` through any means, as long as you can use it in python.
Install `fuzzywuzzy`, `python-Levenshtein`, and `ytmusicapi`.

#### Step 1: Collect Spotify playlist details
Run [`spotify-playlister.py`](spotify-playlister.py) to get the spotify playlist details into a file.
```
python spotify-playlister.py {spotify api key} {spotify playlist id}
```

#### Step 2: Collect YT IDs
Next, run [`spotify-to-yt.py`](spotify-to-yt.py) to collect all the YT video ids from the songs.
```
python spotify-to-yt.py {output file from step 1}
```

#### Step 3: Save YT IDs to a YT Playlist
Finally, run [`yt-ids-to-playlist.py`](yt-ids-to-playlist.py) to save all YT video ids to a YT playlist.
You will be asked to provide browser cookies from a POST request (`/browse`) on (YouTube Music)[https://music.youtube.com/].
See [the ytmusicapi docs](https://ytmusicapi.readthedocs.io/en/stable/setup.html) for in-depth setup instructions.
```
python yt-ids-to-playlist.py {output file from step 2}
```

