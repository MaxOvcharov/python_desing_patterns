#!/usr/bin/env python3
"""
EXAMPLE - https://sourcemaking.com/design_patterns/mediator.

Define an object that encapsulates how a set of objects interact.
Mediator promotes loose coupling by keeping objects from referring to
each other explicitly, and it lets you vary their interaction
independently.
"""


class Mediator:
    """
    Implement cooperative behavior by coordinating Colleague objects.
    Know and maintains its colleagues.
    """

    def __init__(self):
        self._colleague_1 = Colleague1(self)
        self._colleague_2 = Colleague2(self)

    def __str__(self):
        return f'Col1: {self._colleague_1.__dict__}, Col2: {self._colleague_2.__dict__}'


class Colleague1:
    """
    Know its Mediator object.
    Communicate with its mediator whenever it would have otherwise
    communicated with another colleague.
    """

    def __init__(self, mediator):
        self._mediator = mediator


class Colleague2:
    """
    Know its Mediator object.
    Communicate with its mediator whenever it would have otherwise
    communicated with another colleague.
    """

    def __init__(self, mediator):
        self._mediator = mediator


def main():
    mediator = Mediator()
    print(mediator)


if __name__ == "__main__":
    main()
