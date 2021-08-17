from argparse import ArgumentParser
from os import path
from time import sleep
from youtube_playlist import YoutubePlaylist, ExtendedSearchMode


if __name__ == "__main__":
    parser = ArgumentParser(description='Download playlists using a query')
    parser.add_argument('dir', type=str, help='Download Directory')
    parser.add_argument('query', type=str, help='Playlist search query')
    parser.add_argument('--quality', type=str,
                        default='normal',
                        help='Allowed values: normal, high. Defaults to normal.')
    parser.add_argument('--type', type=str,
                        default='playlists',
                        help=f'Allowed values: videos, creativeCommons, playlists. Defaults to playlists.')
    args = parser.parse_args()
    youtubePlaylist = YoutubePlaylist(args.quality,
                                      path.join(args.dir, ''))
    retries = 0
    while retries < 5:
        try:
            youtubePlaylist.download(args.query, args.search_type)
            retries = 0
        except Exception as error:
            print(error, ' Waiting 60s.')
            retries = retries + 1
            sleep(60)
