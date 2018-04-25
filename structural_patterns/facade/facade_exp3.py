# coding: utf-8
"""
Example from - https://github.com/pkolt/design_patterns/blob/master/structural/facade.py

Фасад (Facade) - паттерн, структурирующий объекты.

Предоставляет унифицированный интерфейс вместо набора интерфейсов некоторой подсистемы.
Фасад определяет интерфейс более высокого уровня, который упрощает использование подсистемы.
"""


class Paper(object):
    """Бумага"""
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def draw(self, text):
        if self._count > 0:
            self._count -= 1
            print(text)


class Printer(object):
    """Принтер"""

    @staticmethod
    def error(msg):
        print(f'\n\n!!!\tОшибка: {msg}\t!!!\n\n')

    def print_(self, paper, text):
        if paper.get_count() > 0:
            paper.draw(text)
        else:
            self.error('Бумага закончилась')


class Facade(object):
    def __init__(self, papers=1):
        self._printer = Printer()
        self._paper = Paper(papers)

    def write(self, text):
        self._printer.print_(self._paper, text)


def main():
    papers = 10
    f = Facade(10)
    for _ in range(papers + 1):
        f.write('Hello world!')  # Hello world!


if __name__ == '__main__':
    main()
