from argparse import ArgumentParser
from time import sleep
from youtube_playlist import YoutubePlaylist


DEFAULT_YOUTUBE_STREAM_AUDIO = 140

if __name__ == "__main__":
    parser = ArgumentParser(description='Download playlists using a query')
    parser.add_argument('dir', type=str, help='Download Directory')
    parser.add_argument('query', type=str, help='Playlist search query')
    parser.add_argument('--audio', type=int,
                        default=DEFAULT_YOUTUBE_STREAM_AUDIO, help='Youtube stream audio ID')
    args = parser.parse_args()
    youtubePlaylist = YoutubePlaylist(
        str(args.audio), args.dir)

    retries = 0
    while retries < 5:
        try:
            youtubePlaylist.download(
                youtubePlaylist.search(args.query))
            retries = 0
        except Exception as error:
            print(error)
            retries = retries + 1
            sleep(60)
            continue
