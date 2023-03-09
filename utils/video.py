from googleapiclient.discovery import build
from utils.youtube_class_abstract import Youtube_class
from utils.config import api_key as key_for_youtube


class Video(Youtube_class):
    """
    Класс Video для работы с видео youtube. Унаследован от абстрактного класса Youtube_class.
    Инициализируется по id видео.

    Обязательные методы:

    - get_service- метод класса для получения объекта build, через который 
    осуществляется доступ к сервису youtube
    - get_api_key - метод класса для получения значения API ключа, который 
    задается в файле config.py

    Атрибуты:
    - api_key - атрибут класса - API ключ для доступа к сервису youtube.
    - video_id - id видео
    - youtube - объект для работы с youtube

    Методы:
     - __init__- инициализация экземляра класса
     - get_video_statistic - метод получения статистики видео по его id. 
     В случае некорректного id все атрибуты экземпляра класса Video, кроме id,
      становятся None.
     - __repr__ - метод возвращает представление объекта Video
     - __str__ - метод возвращает строку для печати для объекта Video
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

    def __init__(self, video_id: str) -> None:
        """инициализация класса.
        youtube - объект для работы с youtube"""
        self.set_api_key()
        self.video_id = video_id
        self.youtube = self.get_service()
        self.get_video_statistic()

    def get_video_statistic(self) -> None:
        """
        Метод получения статистики видео по его id.
        Атрибуты:
        - video_id - id видео из ютуб
        - video_name -название видео
        - video_count - количество просмотров
        - video_likes - количество лайков
        """
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics', \
                id=self.video_id).execute()
            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.video_likes: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
        except:
            # загрузка видео по id не удалась
            self.video_name = None
            self.video_count = None
            self.video_likes = None
            self.video_title = None

    def __repr__(self) -> str:
        """метод возвращает представление объекта Video"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self) -> str:
        """метод возвращает строку для печати для объекта Video"""
        return str(self.video_title)


class PLVideo(Video):
    """
    Класс PLVideo для работы с видео и плейлистами youtube.
    Унаследован от Video.
    Атрибуты:
    - self.playlist_id:str - id плейлиста
    - playlist_name:str - название плейлиста
    Методы:
    - __init__() - - инициализация экземляра класса
    - get_playlist_statistic() - метод получения статистики для видео из плейлиста
    - __repr__() - метод возвращает представление объекта Video
    - __str__() - метод возвращает строку для печати для объекта Video
    """
    def __init__(self, video_id: str, playlist_id: str) -> None:
        "инициализация объекта класса PLVideo"
        Video.__init__(self, video_id)
        self.playlist_id = playlist_id
        self.get_playlist_statistic()

    def get_playlist_statistic(self) -> None:
        """
        метод получения статистики для видео из плейлиста.
         Атрибуты:
        - playlist_name - название плейлиста
        """
        playlist = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.playlist_name = playlist['items'][0]['snippet']['title']

    def __repr__(self) -> None:
        """метод возвращает представление объекта PLVideo"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def __str__(self) -> str:
        """метод возвращает строку для печати для объекта PLVideo"""
        return f"{self.video_title} ({self.playlist_name})"
