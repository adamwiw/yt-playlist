from argparse import ArgumentParser
from os import path
from time import sleep
from youtube_playlist import *


def parse_args() -> dict:
    parser = ArgumentParser(description='Download from youtube using a query')
    parser.add_argument('dir', type=str, help='Download Directory')
    parser.add_argument('query', type=str, help='Search query')
    parser.add_argument('--quality', type=str,
                        default='normal',
                        help='Allowed values: normal, high. Defaults to normal.')
    parser.add_argument('--type', type=str,
                        default='playlists',
                        help=f'Allowed values: videos, creative_commons, playlists. Defaults to playlists.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        stream_audio = getattr(StreamId, args.quality)
        search_preferences = getattr(ExtendedSearchMode, args.type)
        youtube_playlist = YoutubePlaylist(stream_audio,
                                        path.join(args.dir, ''))
        retries = 0
        while retries < 5:
            try:
                youtube_playlist.download(args.query, search_preferences)
                retries = 0
            except Exception as error:
                print(error, ' Waiting 60s.')
                retries = retries + 1
                sleep(60)
    except Exception:
        print('Invalid parameters')
