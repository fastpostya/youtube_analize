from utils.channel import Channel
from config import path_json


def main():
    # Задание 1
    # # channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
    channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'    # Редакция

    channel = Channel(channel_id)
    # channel.save_json_in_file(path_json)
    # #channel.print_info()

    vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')


    # Задание 2
    # #vdud.print_info()
    # print(vdud.title)
    # print(vdud.video_count)
    # print(vdud.url) 

    # # менять не можем
    # vdud.__id= 'Новое название'
    # print(vdud.__id)

    # # можем получить объект для работы с API вне класса
    # print(Channel.get_service())
    # #print(vdud.get_service())

    # # создать файл 'vdud.json' с данными по каналу
    # vdud.save_json_in_file('vdud.json')
    
    # Задание 3
    print(vdud)
    print(channel)
    print(vdud == channel)
    print(vdud > channel)
    print(vdud < channel)
    print(vdud + channel)


if __name__ == "__main__":
    main()
