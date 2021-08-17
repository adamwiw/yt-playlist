import re
from pytube import Playlist
from youtubesearchpython import PlaylistsSearch


class YoutubePlaylist:
    def __init__(self, youtubeStreamAudio: str, downloadDir: str) -> None:
        self.__youtubeStreamAudio = youtubeStreamAudio
        self.__downloadDir = downloadDir

    def __download(self,
                   videos: list,
                   page: int,
                   resultsPosition: int,
                   results: list,
                   playlistPosition: int,
                   playlistLength: int,
                   title: str,
                   printTemplate=None) -> None:
        for video in videos:
            if printTemplate:
                print(printTemplate(str(page),
                                    str(resultsPosition),
                                    str(len(results)),
                                    str(playlistPosition),
                                    str(playlistLength),
                                    title,
                                    video.title))
            audioStream = video.streams.get_by_itag(
                self.__youtubeStreamAudio)
            print(audioStream.download(
                output_path=self.__downloadDir + str(page)))
            playlistPosition = playlistPosition + 1

    def __get_playlist(self, result: dict) -> Playlist:
        playlist = Playlist(result['link'])
        playlist._video_regex = re.compile(
            r'"url":"(/watch\?v=[\w-]*)')
        return playlist

    def __loop(self, playlistsSearch: PlaylistsSearch, printTemplate=None) -> None:
        page = 0
        while playlistsSearch.next():
            resultsPosition = 0
            page = page + 1
            results = playlistsSearch.result()['result']
            for result in results:
                playlist = self.__get_playlist(result)
                playlistLength = len(playlist.videos)
                resultsPosition = resultsPosition + 1
                playlistPosition = 0
                self.__download(playlist.videos,
                                page,
                                resultsPosition,
                                results,
                                playlistPosition,
                                playlistLength,
                                result['title'],
                                printTemplate)

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
        self.__loop(playlistsSearch, self.__lineTemplate)
