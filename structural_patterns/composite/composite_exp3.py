#!/usr/bin/env python3
"""
Example from - https://github.com/azmikamis/pipbook/edit/master/any/stationery1.py
"""
import abc
import sys


class AbstractItem(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def composite(self):
        pass

    def __iter__(self):
        return iter([])


class SimpleItem(AbstractItem):

    def __init__(self, name, price=0.00):
        self.name = name
        self.price = price

    @property
    def composite(self):
        return False

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name), file=file)


class AbstractCompositeItem(AbstractItem):

    def __init__(self, *items):
        self.children = []
        if items:
            self.add(*items)

    def add(self, first, *items):
        self.children.append(first)
        if items:
            self.children.extend(items)

    def remove(self, item):
        self.children.remove(item)

    def __iter__(self):
        return iter(self.children)


class CompositeItem(AbstractCompositeItem):

    def __init__(self, name, *items):
        super().__init__(*items)
        self.name = name

    @property
    def composite(self):
        return True

    @property
    def price(self):
        return sum(item.price for item in self)

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name), file=file)
        for child in self:
            child.print(indent + "      ")


def main():
    pencil = SimpleItem("Pencil", 0.40)
    ruler = SimpleItem("Ruler", 1.60)
    eraser = SimpleItem("Eraser", 0.20)
    pencil_set = CompositeItem("Pencil Set", pencil, ruler, eraser)
    box = SimpleItem("Box", 1.00)
    boxed_pencil_set = CompositeItem("Boxed Pencil Set", box, pencil_set)
    boxed_pencil_set.add(pencil)
    for item in (pencil, ruler, eraser, pencil_set, boxed_pencil_set):
        item.print()


if __name__ == "__main__":
    main()
