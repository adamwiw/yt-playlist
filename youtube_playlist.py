import re
from pytube import Playlist
from youtubesearchpython import PlaylistsSearch


class YoutubePlaylist:
    def __init__(self, youtubeStreamAudio: str, downloadDir: str) -> None:
        self.__youtubeStreamAudio = youtubeStreamAudio
        self.__downloadDir = downloadDir

    def __download(self, playlistsSearch: PlaylistsSearch, printTemplate=None) -> None:
        page = 0
        while playlistsSearch.next():
            resultsPosition = 0
            page = page + 1
            results = playlistsSearch.result()['result']
            for result in results:
                playlist = Playlist(result['link'])
                # this fixes the empty playlist.videos list
                playlist._video_regex = re.compile(
                    r"\"url\":\"(/watch\?v=[\w-]*)")
                playlistLength = len(playlist.video_urls)
                resultsPosition = resultsPosition + 1
                playlistPosition = 0
                for video in playlist.videos:
                    if printTemplate:
                        print(printTemplate(
                            str(page),
                            str(resultsPosition),
                            str(len(results)),
                            str(playlistPosition),
                            str(playlistLength),
                            result['title'],
                            video.title
                        ))
                    audioStream = video.streams.get_by_itag(
                        self.__youtubeStreamAudio)
                    print(audioStream.download(
                        output_path=self.__downloadDir + str(page)))
                    playlistPosition = playlistPosition + 1

    def __lineTemplate(
        self,
        page: str,
        searchPosition: str,
        results: str,
        playlistPosition: str,
        playlistLength: str,
        playlistTitle: str,
        videoTitle: str
    ) -> set:
        return (f'page {page}',
                f'playlist {searchPosition}/{results}',
                f'position {playlistPosition}/{playlistLength}',
                f'{playlistTitle}: {videoTitle}')

    def search(self, query) -> PlaylistsSearch:
        return PlaylistsSearch(query)

    def download(self, playlistsSearch: PlaylistsSearch) -> None:
        self.__download(playlistsSearch, self.__lineTemplate)
