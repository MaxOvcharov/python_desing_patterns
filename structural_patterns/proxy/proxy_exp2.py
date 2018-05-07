# coding: utf-8

"""
Example from - https://github.com/pkolt/design_patterns/blob/master/structural/proxy.py

Заместитель (Proxy, Surrogate) - паттерн, структурирующий объекты.
Является суррогатом другого объекта и контролирует доступ к нему.
"""

import abc
from functools import partial


class ImageBase(metaclass=abc.ABCMeta):
    """Абстрактное изображение"""

    @classmethod
    def create(cls, width, height):
        """Создает изображение"""
        return cls(width, height)

    @abc.abstractmethod
    def draw(self, x, y, color):
        """Рисует точку заданным цветом"""
        pass

    @abc.abstractmethod
    def fill(self, color):
        """Заливка цветом"""
        pass

    @abc.abstractmethod
    def save(self, filename):
        """Сохраняет изображение в файл"""
        pass


class Image(ImageBase):
    """Изображение"""
    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)

    def draw(self, x, y, color):
        print(f'Рисуем точку; координаты: ({x}, {y}); цвет: {color}')

    def fill(self, color):
        print(f'Заливка цветом {color}')

    def save(self, filename):
        print(f'Сохраняем изображение в файл {filename}')


class ImageProxy(ImageBase):
    """
    Заместитель изображения. Откладывает выполнение
      операций над изображением до момента его сохранения.
    """
    def __init__(self, *args, **kwargs):
        self._image = Image(*args, **kwargs)
        self.operations = []

    def draw(self, *args):
        func = partial(self._image.draw, *args)
        self.operations.append(func)

    def fill(self, *args):
        func = partial(self._image.fill, *args)
        self.operations.append(func)

    def save(self, filename):
        # выполняем все операции над изображением
        [func() for func in self.operations]
        # сохраняем изображение
        self._image.save(filename)


def main():
    img = ImageProxy(200, 200)
    img.fill('gray')
    img.draw(0, 0, 'green')
    img.draw(0, 1, 'green')
    img.draw(1, 0, 'green')
    img.draw(1, 1, 'green')
    img.save('image.png')


if __name__ == '__main__':
    main()

