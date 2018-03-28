#!/usr/bin/env python3
"""
Example from https://github.com/azmikamis/pipbook/blob/master/any/barchart2.py

Мост (Bridge) - паттерн, структурирующий объекты.
Основная задача - отделить абстракцию от её реализации так,
чтобы то и другое можно было изменять независимо.
"""

import abc
import os
import re
import sys
import tempfile
import tkinter as tk

from collections import collections

WORD_PAT = re.compile(r"\W+")

if sys.version_info[:2] >= (3, 3):
    def has_methods(*methods):

        def decorator(base_cls):

            def __subclasshook__(cls, subcls):
                if cls is base_cls:
                    attributes = collections.ChainMap(
                        *(Superclass.__dict__ for Superclass in subcls.__mro__)
                    )
                    if all(method in attributes for method in methods):
                        return True

                return NotImplemented

            base_cls.__subclasshook__ = classmethod(__subclasshook__)
            return base_cls

        return decorator
else:
    def has_methods(*methods):

        def decorator(base_cls):

            def __subclasshook__(cls, subcls):
                if cls is base_cls:
                    needed = set(methods)
                    for Superclass in subcls.__mro__:
                        for method in needed.copy():
                            if method in Superclass.__dict__:
                                needed.discard(method)
                        if not needed:
                            return True

                return NotImplemented

            base_cls.__subclasshook__ = classmethod(__subclasshook__)
            return base_cls

        return decorator


@has_methods("initialize", "draw_caption", "draw_bar", "finalize")
class BarRenderer(metaclass=abc.ABCMeta):
    pass


class BarCharter:

    def __init__(self, renderer):
        self.__renderer = renderer

    def render(self, caption, pairs):
        maximum = max(value for _, value in pairs)
        self.__renderer.initialize(len(pairs), maximum)
        self.__renderer.draw_caption(caption)
        for name, value in pairs:
            self.__renderer.draw_bar(name, value)

        self.__renderer.finalize()


class TextBarRenderer:

    def __init__(self, scale_factor=40):
        self.scaleFactor = scale_factor
        self.scale = 0

    def initialize(self, bars, maximum):
        assert bars > 0 and maximum > 0
        self.scale = self.scaleFactor / maximum

    def draw_caption(self, caption):
        print("{0:^{2}}\n{1:^{2}}".format(caption, "=" * len(caption), self.scaleFactor))

    def draw_bar(self, name, value):
        print("{} {}".format("*" * int(value * self.scale), name))

    def finalize(self):
        pass


class ImageBarRenderer:

    COLORS = ("red", "green", "blue", "yellow", "magenta", "cyan")

    def __init__(self, step_height=10, bar_width=30, bar_gap=2):
        self.stepHeight = step_height
        self.barWidth = bar_width
        self.barGap = bar_gap
        self.index = self.width = self.height = 0
        self.image = None
        self.gui = None
        self.filename = ''
        self.inGui = False

    def initialize(self, bars, maximum):
        assert bars > 0 and maximum > 0

        if tk._default_root is None:
            self.gui = tk.Tk()
        else:
            self.gui = tk._default_root
            self.inGui = True

        self.index = 0
        self.width = bars * (self.barWidth + self.barGap)
        self.height = maximum * self.stepHeight
        self.image = tk.PhotoImage(width=self.width, height=self.height)
        self.image.put("white", (0, 0, self.width, self.height))

    def draw_caption(self, caption):
        self.filename = \
            os.path.join(tempfile.gettempdir(), WORD_PAT.sub("_", caption) + ".gif")

    def draw_bar(self, _, value):
        color = \
            ImageBarRenderer.COLORS[self.index % len(ImageBarRenderer.COLORS)]
        x0 = self.index * (self.barWidth + self.barGap)
        x1 = x0 + self.barWidth
        y0 = self.height - (value * self.stepHeight)
        y1 = self.height - 1
        self.image.put(color, (x0, y0, x1, y1))
        self.index += 1

    def finalize(self):
        self.image.write(self.filename, "gif")
        print("wrote", self.filename)
        if not self.inGui:
            self.gui.quit()


def main():
    pairs = (
        ("Mon", 16), ("Tue", 17), ("Wed", 19),
        ("Thu", 22), ("Fri", 24), ("Sat", 21), ("Sun", 19)
    )
    text_bar_charter = BarCharter(TextBarRenderer())
    text_bar_charter.render("Forecast 6/8", pairs)
    image_bar_charter = BarCharter(ImageBarRenderer())
    image_bar_charter.render("Forecast 6/8", pairs)


if __name__ == "__main__":
    main()
