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
                   template=None) -> None:
        for video in videos:
            playlistPosition = playlistPosition + 1
            try:
                if template:
                    print(template(str(page),
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
            except Exception as error:
                print(error)

    def __get_playlist(self, result: dict) -> Playlist:
        playlist = Playlist(result['link'])
        playlist._video_regex = re.compile(
            r'"url":"(/watch\?v=[\w-]*)')
        return playlist

    def __template(
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

    def __loop(self, playlistsSearch: PlaylistsSearch, templateFunction=None) -> None:
        page = 0
        while playlistsSearch.next():
            resultsPosition = 0
            page = page + 1
            try:
                results = playlistsSearch.result()['result']
                for result in results:
                    playlistPosition = 0
                    resultsPosition = resultsPosition + 1
                    playlist = self.__get_playlist(result)
                    playlistLength = len(playlist.videos)
                    self.__download(playlist.videos,
                                    page,
                                    resultsPosition,
                                    results,
                                    playlistPosition,
                                    playlistLength,
                                    result['title'],
                                    templateFunction)
            except Exception as error:
                print(error)

    def download(self, query: str) -> None:
        self.__loop(PlaylistsSearch(query), self.__template)
