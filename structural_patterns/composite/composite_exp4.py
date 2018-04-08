#!/usr/bin/env python3
"""
Example from - https://github.com/azmikamis/pipbook/edit/master/any/stationery2.py
"""
from itertools import chain
import sys


class Item:

    def __init__(self, name, *items, price=0.00):
        self.name = name
        self.price = price
        self.children = []
        if items:
            self.add(*items)

    @classmethod
    def create(cls, name, price):
        return cls(name, price=price)

    @classmethod
    def compose(cls, name, *items):
        return cls(name, *items)

    @property
    def composite(self):
        return bool(self.children)

    def add(self, first, *items):
        self.children.extend(chain((first,), items))

    def remove(self, item):
        self.children.remove(item)

    def __iter__(self):
        return iter(self.children)

    @property
    def price(self):
        res = sum(item.price for item in self) if self.children else self.__price
        return res

    @price.setter
    def price(self, price):
        self.__price = price

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name), file=file)
        for child in self:
            child.print(indent + "      ")


def make_item(name, price):
    return Item(name, price=price)


def make_composite(name, *items):
    return Item(name, *items)


def main():
    pencil = Item.create("Pencil", 0.40)
    ruler = Item.create("Ruler", 1.60)
    eraser = make_item("Eraser", 0.20)
    pencil_set = Item.compose("Pencil Set", pencil, ruler, eraser)
    box = Item.create("Box", 1.00)
    boxed_pencil_set = make_composite("Boxed Pencil Set", box, pencil_set)
    boxed_pencil_set.add(pencil)
    for item in (pencil, ruler, eraser, pencil_set, boxed_pencil_set):
        item.print()
    assert not pencil.composite
    pencil.add(eraser, box)
    assert pencil.composite
    pencil.print()
    pencil.remove(eraser)
    assert pencil.composite
    pencil.remove(box)
    assert not pencil.composite
    pencil.print()


if __name__ == "__main__":
    main()
