# coding: utf-8

"""
Example from - https://github.com/pkolt/design_patterns/blob/master/structural/decorator.py

Декоратор (Decorator, Wrapper) - паттерн, структурирующий объекты.

Динамически добавляет объекту новые обязанности.
  Является гибкой альтернативой порождению подклассов с целью
  расширения функциональности.
"""


class Man(object):
    def __init__(self, name):
        self._name = name

    def say(self):
        print(f'Привет! Меня зовут {self._name}!')


class Jetpack(object):
    """Реактивный ранец"""
    def __init__(self, man_cls):
        self._man_cls = man_cls

    def __getattr__(self, item):
        return getattr(self._man_cls, item)

    def fly(self):
        # расширяем функциональность объекта добавляя возможность летать
        print(f'{self._man_cls._name} летит на реактивном ранце!')


if __name__ == '__main__':
    man = Man('Super Man')
    man_jetpack = Jetpack(man)
    man_jetpack.say()  # Привет! Меня зовут Виктор!
    man_jetpack.fly()  # Виктор летит на реактивном ранце!
