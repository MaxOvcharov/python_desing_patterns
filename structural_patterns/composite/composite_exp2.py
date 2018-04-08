#!/usr/bin/env python3
# coding: utf-8
"""
Example from - https://github.com/pkolt/design_patterns/edit/master/structural/composite.py

Компоновщик (Composite) - паттерн, структурирующий объекты.

Компонует объекты в древовидные структуры для представления иерархий часть-целое.
Позволяет клиентам единообразно трактовать индивидуальные и составные объекты.
"""
import abc


# Класс представляющий одновременно примитивы и контейнеры
class Graphic(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass


class Line(Graphic):
    def draw(self):
        print('Линия')


class Rectangle(Graphic):
    def draw(self):
        print('Прямоугольник')


class Text(Graphic):
    def draw(self):
        print('Текст')


class Picture(Graphic):
    def __init__(self):
        self._children = []

    def draw(self):
        print('Изображение')
        # вызываем отрисовку у вложенных объектов
        for obj in self._children:
            obj.draw()

    def add(self, obj):
        if isinstance(obj, Graphic) and obj not in self._children:
            self._children.append(obj)

    def remove(self, obj):
        index = self._children.index(obj)
        del self._children[index]

    def get_child(self, index):
        return self._children[index]


pic = Picture()
pic.add(Line())
pic.add(Rectangle())
pic.add(Text())
pic.draw()
# Изображение
# Линия
# Прямоугольник
# Текст

line = pic.get_child(0)
line.draw()  # Линия
