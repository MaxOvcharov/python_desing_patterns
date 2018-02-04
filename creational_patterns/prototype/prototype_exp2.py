#!/usr/bin/env python3
"""
Example from http://www.qtrac.eu/pipbook.html
"""
import sys
import copy


class Point:

    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_object(Class, *args, **kwargs):
    return Class(*args, **kwargs)


# Seven ways of copy "Point" instance
cl_name, x, y = "Point", 1, 1
point1 = Point(x, y)
point2 = eval(f"{cl_name}({x + 2}, {y + 2})")
point3 = getattr(sys.modules[__name__], cl_name)(x + 3, y + 3)
point4 = globals()[cl_name](x + 4, y + 4)
point5 = make_object(Point, x + 5, y + 5)
point6 = copy.deepcopy(point5)
point6.x = x + 6
point6.y = y + 6

# Python way
point7 = point1.__class__(x + 7, y + 7)



