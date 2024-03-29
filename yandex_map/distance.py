from math import cos, radians


def distance_two_point(point1: tuple[int], point2: tuple[int]):
    """
    Аргументы точек принимают кортежи где первый элемент широта 
    а второй - долгота. Функция нахождения расстояния от одной точки до другой 
    в метрах. Для определения км в 1 градусе по параллелям необходимо умножить 
    111,3 на косинус градусной меры параллели.
    """
    oy = ((point1[1] * cos(radians(point1[1])) * 111)  - (point2[1] * cos(radians(point2[1])) * 111))
    ox = ((point1[0])  - (point2[0])) * 111
    return int(((oy ** 2 + ox ** 2) ** 0.5) * 1000)


print(distance_two_point((58.548646, 31.314992), (58.545974, 31.311246)))