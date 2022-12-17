#!/bin/python
from ytmusicapi import YTMusic
from sys import argv

def main(filename):

    # ask user for personal youtube headers
    YTMusic.setup()

    # get all the video ids in the file
    with open(filename) as f:
        lines = f.readlines()
        #  video_ids = list(map(lambda x: x.split()[-1], lines))
        video_ids = []
        for line in lines:
            if line.endswith('(?)'):
                print('"(?)" contained in music file. Please use video ids you know are correct.')
                print('Stopping execution.')
                return
            video_id = line[-1]
            video_ids.append(video_id)

    # create the playlist
    ytm = YTMusic()
    title = input('Playlist title: ')
    desc = input('Playlist Description: ')
    yt_id = ytm.create_playlist(title, desc, video_ids=video_ids)

    # return the playlist id if it was created successfully
    if isinstance(yt_id, str):
        return yt_id
    print('Error occurred:', yt_id)
    return None

if __name__ == '__main__':
    main(argv[1])

