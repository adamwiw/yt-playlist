import re
from pytube import Playlist, YouTube
from youtubesearchpython import CustomSearch
from youtubesearchpython.internal.constants import SearchMode


class ExtendedSearchMode(SearchMode):
    creative_commons = 'EgQQATAB'


class StreamId:
    normal = '140'
    high = '141'


class YoutubePlaylist:
    def __init__(self, stream_audio: str, download_dir: str) -> None:
        self.__stream_audio = stream_audio
        self.__download_dir = download_dir

    def __download(self, video, page: str) -> str:
        audio_stream = video.streams.get_by_itag(
            self.__stream_audio)
        return audio_stream.download(
            output_path=self.__download_dir + page)

    def __loop_playlist(self,
                       videos: list,
                       page: int,
                       results_position: int,
                       results_length: int,
                       title: str) -> None:
        playlist_length = len(videos)
        for playlist_position, video in enumerate(videos):
            print((f'page {page}',
                   f'result {results_position}/{results_length}',
                   f'position {playlist_position}/{playlist_length}' if playlist_length > 1 else '',
                   f'{title}: {video.title}' if video.title != title else title))
            try:
                print(self.__download(video, page))
            except Exception as error:
                print(error)

    def __get_videos(self, link: str, search_preferences: str) -> list:
        if search_preferences == ExtendedSearchMode.playlists:
            playlist = Playlist(link)
            playlist._video_regex = re.compile(
                r'"url":"(/watch\?v=[\w-]*)')
            return playlist.videos
        if search_preferences in [ExtendedSearchMode.videos, ExtendedSearchMode.creative_commons]:
            return [YouTube(link)]

    def download(self, query: str, search_preferences: str, page_max=100) -> None:
        playlists_search = CustomSearch(query, search_preferences)
        page = 1
        while page in range(1, page_max) and playlists_search.next():
            results = playlists_search.result()['result']
            for results_position, result in enumerate(results):
                videos = self.__get_videos(result['link'], search_preferences)
                self.__loop_playlist(videos,
                                    page,
                                    results_position + 1,
                                    len(results),
                                    result['title'])
