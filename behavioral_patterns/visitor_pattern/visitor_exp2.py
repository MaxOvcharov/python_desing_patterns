#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/visitor.py.

Постетитель (Visitor) - паттерн поведения объектов.
Описывает операцию, выполняемую с каждым объектом из некоторой структуры.
Паттерн посетитель позволяет определить новую операцию,
не изменяя классы этих объектов.
"""


class FruitVisitor:
    """Посетитель"""

    def draw(self, fruit):
        methods = {
            Apple: self.draw_apple,
            Pear: self.draw_pear,
        }
        draw = methods.get(type(fruit), self.draw_unknown)
        draw(fruit)

    def draw_apple(self, fruit):
        print(f'Яблоко - {fruit}')

    def draw_pear(self, fruit):
        print(f'Груша- {fruit}')

    def draw_unknown(self, fruit):
        print(f'Фрукт- {fruit}')


class Fruit:
    """Фрукты"""

    def draw(self, visitor):
        visitor.draw(self)


class Apple(Fruit):
    """Яблоко"""


class Pear(Fruit):
    """Груша"""


class Banana(Fruit):
    """Банан"""


def main():
    visitor = FruitVisitor()

    apple = Apple()
    apple.draw(visitor)
    # Яблоко

    pear = Pear()
    pear.draw(visitor)
    # Груша

    banana = Banana()
    banana.draw(visitor)
    # Фрукт


if __name__ == '__main__':
    main()
