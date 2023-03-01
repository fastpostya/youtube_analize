from config import api_key as key_for_youtube
from googleapiclient.discovery import build


class Video():
    """
    Класс Video для работы с видео youtube.
    Атрибуты:
    - api_key - API ключ для доступа к сервису youtube.
    - get_service() - метод класса для получения объекта build,
     через который осуществляется доступ к сервису youtube
     - set_api_key() -метод класса для получения значения API ключа из config.py
     - __init__()- инициализация экземляра класса
     - get_video_statistic() - метод получения статистики видео по его id
     - __repr__() - метод возвращает представление объекта Video
     - __str__() - метод возвращает строку для печати для объекта Video
    """
    api_key = ""

    @classmethod
    def get_service(cls):
        """метод класса возвращает объект для работы с youtube"""
        with build('youtube', 'v3', developerKey=cls.api_key) as youtube:
            return youtube

    @classmethod
    def set_api_key(cls):
        """метод класса возвращает ключ для работы с youtube"""
        cls.api_key = key_for_youtube
        return cls.api_key

    def __init__(self, video_id):
        """инициализация класса.
        youtube - объект для работы с youtube"""
        self.set_api_key()
        self.video_id = video_id
        self.youtube = self.get_service()
        self.get_video_statistic()

    def get_video_statistic(self):
        """
        Метод получения статистики видео по его id.
        Атрибуты:
        - video_id - id видео из ютуб
        - video_name -название видео
        - video_count - количество просмотров
        - video_likes - количество лайков
        """
        video_response = self.youtube.videos().list(part='snippet,statistics', \
            id=self.video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.video_likes: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __repr__(self):
        """метод возвращает представление объекта Video"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self):
        """метод возвращает строку для печати для объекта Video"""
        return self.video_title


class PLVideo(Video):
    """
    Класс PLVideo для работы с видео и плейлистами youtube.
    Унаследован от Video.
    Атрибуты:
    - __init__() - - инициализация экземляра класса
    - get_playlist_statistic() - метод получения статистики для видео из плейлиста
    - __repr__() - метод возвращает представление объекта Video
    - __str__() - метод возвращает строку для печати для объекта Video
    """
    def __init__(self, video_id, playlist_id):
        "инициализация объекта класса PLVideo"
        Video.__init__(self, video_id)
        self.playlist_id = playlist_id
        self.get_playlist_statistic()

    def get_playlist_statistic(self):
        """
        метод получения статистики для видео из плейлиста.
         Атрибуты:
        - playlist_name - название плейлиста
        """
        playlist = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']

        # playlist_videos = self.youtube.playlistItems().list(playlistId=\
        #     self.playlist_id, part='contentDetails', maxResults=50,).execute()
        
        # получить все id видеороликов из плейлиста
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items'] if video['contentDetails']['videoId'] == self.video_id]
        
       

    def __repr__(self):
        """метод возвращает представление объекта PLVideo"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self):
        """метод возвращает строку для печати для объекта PLVideo"""
        return f"{self.video_title} ({self.playlist_name})"

