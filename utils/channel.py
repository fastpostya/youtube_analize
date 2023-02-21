import json
import os
from googleapiclient.discovery import build
#from config import youtube_api


class Channel():
    """Класс Channel для работы с каналами youtube. Для корректной работы
    необходимо поместить значение API key youtube в переменную среды YOUTUBE_API.
    Объект класса Channel инициализируется с помощью id канала. """
    #api_key = youtube_api
    
    api_key: str = os.getenv('YOUTUBE_API')
   

    def __init__(self, id):
        """инициализация объекта Channel"""
        self.__id = id
        self.json = ""
        # загружаем информацию о канале по его id
        self.get_json_by_id()
        self.title = self.json["items"][0]['snippet']['title']
        self.chanel_description = self.json["items"][0]['snippet']['description']
        self.url = r"https://www.youtube.com/channel/" + self.__id
        self.video_count = self.json["items"][0]["statistics"]["videoCount"]
        self.channel_number_of_views = self.json["items"][0]["statistics"]["viewCount"]


    def save_json_in_file(self, path):
        """метод сохраняет все атрибуты объекта channel, кроме json в файл по адресу path"""
        text = "["
        for dic in self.__dict__:
            if dic != 'json':
                text +=  "{'" + str(dic) + "':'" +str(self.__dict__[dic]) + "'}, \n"
        json_text = text[:-3] + "]"
        with open(path, "w", encoding="UTF-8") as file:
            file.write(str(json_text))   

    
    def get_json_by_id(self):
        """ метод создает специальный объект для работы с API youtube"""
        with build('youtube', 'v3', developerKey=Channel.api_key) as youtube:
            channel = youtube.channels().list(id=self.__id, part='snippet,statistics').execute()
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

    def get_service(self):
        """метод возвращает объект для работы с youtube"""
        # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        with build('youtube', 'v3', developerKey=Channel.api_key) as youtube:
            #channel = youtube.channels().list(id=self.__id, part='snippet,statistics').execute()
            return youtube

