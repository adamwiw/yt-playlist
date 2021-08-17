import re
from pytube import Playlist
from youtubesearchpython import PlaylistsSearch


class YoutubePlaylist:
    def __init__(self, youtubeStreamAudio: str, downloadDir: str) -> None:
        self.__youtubeStreamAudio = youtubeStreamAudio
        self.__downloadDir = downloadDir

    def __download(self, video, page: str) -> str:
        audioStream = video.streams.get_by_itag(
                    self.__youtubeStreamAudio)
        return audioStream.download(
            output_path=self.__downloadDir + page)

    def __printAndDownload(self,
                   videos: list,
                   page: str,
                   resultsPosition: str,
                   resultsLength: str,
                   title: str) -> None:
        playlistLength = str(len(videos))
        for playlistPosition, video in enumerate(videos):
            print((f'page {page}',
                   f'playlist {resultsPosition}/{resultsLength}',
                   f'position {playlistPosition}/{playlistLength}',
                   f'{title}: {video.title}'))
            try:
                print(self.__download(video, page))
            except Exception as error:
                print(error)

    def __get_playlist(self, result: dict) -> Playlist:
        playlist = Playlist(result['link'])
        playlist._video_regex = re.compile(
            r'"url":"(/watch\?v=[\w-]*)')
        return playlist

    def __loop(self, playlistsSearch: PlaylistsSearch) -> None:
        page = 0
        while playlistsSearch.next():
            page = page + 1
            try:
                results = playlistsSearch.result()['result']
                for resultsPosition, result in enumerate(results):
                    videos = self.__get_playlist(result).videos
                    self.__printAndDownload(videos,
                                    str(page),
                                    str(resultsPosition + 1),
                                    str(len(results)),
                                    result['title'])
                    resultsPosition = resultsPosition + 1
            except Exception as error:
                print(error)

    def download(self, query: str) -> None:
        self.__loop(PlaylistsSearch(query), self.__template)
