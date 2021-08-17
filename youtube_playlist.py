import re
from pytube import Playlist, YouTube
from youtubesearchpython import CustomSearch
from youtubesearchpython.internal.constants import SearchMode


class ExtendedSearchMode(SearchMode):
    creativeCommons = 'EgQQATAB'


class StreamId:
    normal = 140
    high = 141


class YoutubePlaylist:
    def __init__(self, quality: str, downloadDir: str) -> None:
        self.__youtubeStreamAudio = getattr(StreamId, quality)
        assert self.__youtubeStreamAudio
        self.__downloadDir = downloadDir

    def __download(self, video, page: str) -> str:
        audioStream = video.streams.get_by_itag(
            self.__youtubeStreamAudio)
        return audioStream.download(
            output_path=self.__downloadDir + page)

    def __loopPlaylist(self,
                       videos: list,
                       page: int,
                       resultsPosition: int,
                       resultsLength: int,
                       title: str) -> None:
        playlistLength = len(videos)
        for playlistPosition, video in enumerate(videos):
            print((f'page {page}',
                   f'result {resultsPosition}/{resultsLength}',
                   f'position {playlistPosition}/{playlistLength}' if playlistLength > 1 else '',
                   f'{title}: {video.title}' if video.title != title else title))
            try:
                print(self.__download(video, page))
            except Exception as error:
                print(error)

    def __get_videos(self, link: str, searchPreferences: str) -> list:
        if searchPreferences == ExtendedSearchMode.playlists:
            playlist = Playlist(link)
            playlist._video_regex = re.compile(
                r'"url":"(/watch\?v=[\w-]*)')
            return playlist.videos
        if searchPreferences in [ExtendedSearchMode.videos, ExtendedSearchMode.creativeCommons]:
            return [YouTube(link)]

    def download(self, query: str, searchType: str, pageMax=100) -> None:
        searchPreferences = getattr(ExtendedSearchMode, searchType)
        assert searchPreferences
        playlistsSearch = CustomSearch(query, searchPreferences)
        page = 1
        while page in range(1, pageMax) and playlistsSearch.next():
            results = playlistsSearch.result()['result']
            for resultsPosition, result in enumerate(results):
                videos = self.__get_videos(result['link'], searchPreferences)
                self.__loopPlaylist(videos,
                                    page,
                                    resultsPosition + 1,
                                    len(results),
                                    result['title'])
