import json
import os
from googleapiclient.discovery import build
from utils.youtube_class_abstract import Youtube_class
from utils.config import api_key as key_for_youtube


class Channel(Youtube_class):
    """Класс Channel для работы с каналами youtube. Унаследован 
    от абстрактного класса Youtube_class. Обязательные методы:
    -get_service- метод класса для получения объекта build,
        через который осуществляется доступ к сервису youtube
    -set_api_key - метод класса для получения значения API ключа,
    который задается в файле config.py
    
    Для корректной работы необходимо поместить значение API key 
    youtube в переменную среды YOUTUBE_API.
    Объект класса Channel инициализируется с помощью id канала. 

    Атрибуты:

    - api_key:str  - атрибут класса. Содержит значение ключа для
    работы с API youtube
    - __id:str  - id youtube-канала. Приватный атрибут.
    - json: str - полученные данные для канала в формате json
    - title: str - название канала
    - chanel_description: str - описание канала
    - url: str - адрес канала в интернете
    - video_count: str  - количество просмотров видео
    - channel_number_of_views: str  - количество просмотров канала

    Методы:
    - __init__ - инициализация объекта Channel
    - save_json_in_file - метод сохраняет все атрибуты объекта channel, 
    кроме json в файл по адресу path 
    - get_json_by_id - метод получает данные о канале в формате json
    используя self.__id - id канала и помещает их в атрибут self.json
    - __repr__ - метод возвращает представление объекта channel
    -  print_info -метод ввыводит на печать содержимое json
    """

    api_key: str = ""
   
    @classmethod
    def set_api_key(cls):
        """метод класса возвращает ключ для работы с youtube"""
        cls.api_key = key_for_youtube
        return cls.api_key

    def __init__(self, id):
        """инициализация объекта Channel"""
        self.__id = id
        self.json = ""
        # загружаем ключ для работы с API youtube
        self.set_api_key()
        # загружаем информацию о канале по его id
        self.get_json_by_id()
        self.title = self.json["items"][0]['snippet']['title']
        self.chanel_description = self.json["items"][0]['snippet']['description']
        self.url = r"https://www.youtube.com/channel/" + self.__id
        self.video_count = self.json["items"][0]["statistics"]["videoCount"]
        self.channel_number_of_views = self.json["items"][0]["statistics"]["viewCount"]

    def save_json_in_file(self, path):
        """метод сохраняет все атрибуты объекта channel, кроме json 
        в файл по адресу path"""
        text = "["
        for dic in self.__dict__:
            if dic != 'json':
                text +=  "{'" + str(dic) + "':'" +str(self.__dict__[dic]) + "'}, \n"
        json_text = text[:-3] + "]"
        with open(path, "w", encoding="UTF-8") as file:
            file.write(str(json_text))

    def get_json_by_id(self):
        """ метод получает данные о канале в формате json
        используя self.__id - id канала и помещает их в атрибут self.json"""
        # 1-й способ
        # with build('youtube', 'v3', developerKey=Channel.api_key) as youtube:
        #     channel = youtube.channels().list(id=self.__id, part='snippet,statistics').execute()
        # 2-й способ
        channel = self.get_service().channels().list(id=self.__id, part='snippet,statistics').execute()
        self.json = channel

    def __repr__(self):
        """метод возвращает представление объекта channel"""
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]

    def print_info(self):
        """метод ввыводит на печать содержимое json"""
        print(self.json)

    @classmethod
    def get_service(cls):
        """метод класса возвращает объект для работы с youtube,
        используя cls.api_key"""
        with build('youtube', 'v3', developerKey=cls.api_key) as youtube:
            return youtube
