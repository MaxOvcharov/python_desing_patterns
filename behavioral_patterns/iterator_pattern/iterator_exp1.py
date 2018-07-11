#!/usr/bin/env python3
# coding: utf-8

"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/iterator.py
Итератор (Iterator) - паттерн поведения объектов.

Предоставляет способ последовательного доступа ко всем элементам составного объекта,
не раскрывая его внутреннего представления.
"""
import abc


class IteratorBase(metaclass=abc.ABCMeta):
    """Базовый класс итератора"""

    @abc.abstractmethod
    def first(self):
        """
        Возвращает первый элемент коллекции. Если элемента не 
          существует возбуждается исключение IndexError.
        """
        pass

    @abc.abstractmethod
    def last(self):
        """
        Возвращает последний элемент коллекции. Если элемента не 
          существует возбуждается исключение IndexError.
        """
        pass

    @abc.abstractmethod
    def next(self):
        """ Возвращает следующий элемент коллекции """
        pass

    @abc.abstractmethod
    def prev(self):
        """ Возвращает предыдущий элемент коллекции """
        pass

    @abc.abstractmethod
    def current_item(self):
        """ Возвращает текущий элемент коллекции """
        pass

    @abc.abstractmethod
    def is_done(self, index):
        """
        Возвращает истину если элемент с указанным индексом 
          существует, иначе ложь
        """
        pass

    @abc.abstractmethod
    def get_item(self, index):
        """
        Возвращает элемент коллекции с указанным индексом, 
          иначе возбуждает исключение IndexError
        """
        pass


class Iterator(IteratorBase):
    def __init__(self, data=None):
        self.data = data or ()
        self._current = 0

    def first(self):
        return self.data[0]

    def last(self):
        return self.data[-1]

    def current_item(self):
        return self.data[self._current]

    def is_done(self, index):
        last_index = len(self.data) - 1
        return 0 <= index <= last_index

    def next(self):
        self._current += 1
        if not self.is_done(self._current):
            self._current = 0
        return self.current_item()

    def prev(self):
        self._current -= 1
        if not self.is_done(self._current):
            self._current = len(self.data) - 1
        return self.current_item()

    def get_item(self, index):
        if not self.is_done(index):
            raise IndexError('Нет элемента с индексом: %d' % index)
        return self.data[index]


it = Iterator(('one', 'two', 'three', 'four', 'five'))
print([it.prev() for _ in range(5)])  # ['five', 'four', 'three', 'two', 'one']
print([it.next() for _ in range(5)])  # ['two', 'three', 'four', 'five', 'one']
