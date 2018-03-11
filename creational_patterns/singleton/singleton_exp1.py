# coding: utf-8

"""
EXAMPLE - https://sourcemaking.com/design_patterns/singleton/python/1

Одиночка (Singleton) - паттерн, порождающий объекты.
Гарантирует, что у класса есть только один экземпляр,
  и предоставляет к нему глобальную точку доступа.
С помощью паттерна одиночка могут быть реализованы многие
  паттерны (абстрактная фабрика, строитель, прототип).
"""


class Singleton(type):
    """
    Define an Instance operation that lets
      clients access its unique instance.
    """
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class MyClass(metaclass=Singleton):

    def __init__(self, name):
        """ Example class. """
        self.name = name

    def get_name(self):
        return self.name


def main():
    m1 = MyClass('Test_singleton_1')
    print(f"Create instance: {m1.get_name()}")
    m2 = MyClass('Test_singleton_2')
    print(f"Create instance: {m2.get_name()}")

    print(f"Check SINGLETON: {m1 is m2}")


if __name__ == "__main__":
    main()
