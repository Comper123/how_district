import requests
import os
from PIL import Image
from random import uniform


api_key = '40d1649f-0493-4b70-98ba-98533de7710b'


def get_coordinates(place: str, format: str="json"):
    """
    Функция возвращает координаты обьекта на карте по его названию
    """
    link = f'http://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={place}&format={format}'
    response = requests.get(link)
    if response:
        data = response.json()
        object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coords = object["Point"]["pos"]
        return list(map(float, coords.split()))
    

def get_map(center: tuple[int], size: tuple[int]=[600, 450], way: tuple[int]=False, spn: str="0.005", map_format: str="map"):
    """
    Функция для создания изображения карты по переданным аргументам

    Параметр map_format может принимать следующие значения:
        map - карта схема местности
        sat - снимок спутника
        trf - карта автодорог
        skl - географические объекты
    """
    # Преобразуем параметры для удобства пользования
    x, y = map(str, center)
    width, height = map(str, size)

    map_link = f"https://static-maps.yandex.ru/1.x/?l={map_format}&ll={x},{y}&size={width},{height}&spn={spn},{spn}"
    # Если передан дополнительный маршрут
    if way:
        map_link += f"&pl={','.join(list(map(str, way)))}"
    content = requests.get(map_link).content
    map_file = f"{x}-{y}.png"
    with open(map_file, 'wb') as map_1:
        map_1.write(content)
    return map_file 


def del_map(map: str):
    """
    Функция удаления изображения файла из файловой системы
    """
    os.remove(map)


def show_map(map: str):
    """
    Функция для просмотра получившейся карты
    """
    with Image.open(map) as img:
        img.show()


def random_spn(start: float, stop: float):
    """
    Функция генерирует случайный коэфициент масштабирования карты 
    исходя из заданных пределов
    """
    return uniform(start, stop)


def get_place(coord: tuple[int], type_place: str="house"):
    """
    Функция распознавания района по переданным координатам
    Исходя из параметра type_place можно получить следующие данные:
        house — дом;
        street — улица;
        metro — станция метро;
        district — район города;
        locality — населенный пункт (город/поселок/деревня/село)
    """
    x, y = list(map(str, coord))
    link = f"http://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={x},{y}&kind={type_place}&format=json"
    response = requests.get(link)
    if response:
        data = response.json()
        object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        dist = object["metaDataProperty"]["GeocoderMetaData"]["text"]
        return dist