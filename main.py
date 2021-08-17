from argparse import ArgumentParser
from os import path
from time import sleep
from youtube_playlist import YoutubePlaylist
from youtubesearchpython.internal.constants import SearchMode


DEFAULT_YOUTUBE_STREAM_AUDIO = 141

if __name__ == "__main__":
    parser = ArgumentParser(description='Download playlists using a query')
    parser.add_argument('dir', type=str, help='Download Directory')
    parser.add_argument('query', type=str, help='Playlist search query')
    parser.add_argument('--audio-id', type=int,
                        default=DEFAULT_YOUTUBE_STREAM_AUDIO,
                        help='Defaults to 256kbps AAC({DEFAULT_YOUTUBE_STREAM_AUDIO})')
    parser.add_argument('--search-preferences', type=str,
                        default=SearchMode.playlists,
                        help=f'Defaults to playlists({SearchMode.playlists})')
    args = parser.parse_args()
    youtubePlaylist = YoutubePlaylist(str(args.audio),
                                      path.join(args.dir, ''))
    retries = 0
    while retries < 5:
        try:
            youtubePlaylist.download(args.query, )
            retries = 0
        except Exception as error:
            print(error, ' Waiting 60s.')
            retries = retries + 1
            sleep(60)
