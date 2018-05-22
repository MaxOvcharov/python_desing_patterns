#!/usr/bin/env python3
"""
EXAMPLE - https://github.com/azmikamis/pipbook/blob/master/any/eventhandler2.py
"""
import functools
import random
import sys
import string

random.seed(917)  # Don't want random for regression tests

MOUSE, KEYPRESS, TIMER, TERMINATE = ("MOUSE", "KEYPRESS", "TIMER", "TERMINATE")


class Event:

    TimerId = 0

    def __init__(self, kind, **kwargs):
        assert kind in {MOUSE, KEYPRESS, TIMER, TERMINATE}
        self.kind = kind
        self.kwargs = kwargs
        if self.kind == TIMER:
            self.kwargs["id"] = Event.TimerId
            Event.TimerId += 1

    def __str__(self):
        if self.kind == MOUSE:
            return "Button {} ({}, {})".format(
                self.kwargs.get("button", 1),
                self.kwargs.get("x", -1),
                self.kwargs.get("y", -1)
            )
        elif self.kind == KEYPRESS:
            return "Key {}{}{}".format(
                "Ctrl+" if self.kwargs.get("ctrl", False) else "",
                "Shift+" if self.kwargs.get("shift", False) else "",
                self.kwargs.get("key", "")
            )
        elif self.kind == TIMER:
            return "Timer {}".format(self.kwargs.get("id", -1))
        elif self.kind == TERMINATE:
            return "Terminate"

    @staticmethod
    def next():
        kinds = ([MOUSE] * 7) + ([KEYPRESS] * 11) + ([TIMER] * 5) + [TERMINATE]
        kind = random.choice(kinds)
        if kind == MOUSE:
            return Event(
                kind, button=random.randint(1, 3),
                x=random.randint(0, 640),
                y=random.randint(0, 480)
            )
        elif kind == KEYPRESS:
            return Event(
                kind, ctrl=random.randint(1, 7) == 1,
                shift=random.randint(1, 5) == 1,
                key=random.choice(string.ascii_lowercase)
            )
        return Event(kind)  # TIMER or TERMINATE


def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        next(generator)
        return generator
    return wrapper


@coroutine
def debug_handler(successor, file=sys.stdout):
    while True:
        event = (yield)
        file.write(f'*DEBUG*: {event}\n')
        successor.send(event)


@coroutine
def mouse_handler(successor=None):
    while True:
        event = (yield)
        if event.kind == MOUSE:
            print(f'Click:   {event}')
        elif successor is not None:
            successor.send(event)


@coroutine
def key_handler(successor=None):
    while True:
        event = (yield)
        if event.kind == KEYPRESS:
            print(f'Press:   {event}')
        elif successor is not None:
            successor.send(event)


@coroutine
def timer_handler(successor=None):
    while True:
        event = (yield)
        if event.kind == TIMER:
            print(f'Timeout: {event}')
        elif successor is not None:
            successor.send(event)


def main():
    print("Handler Chain #1")
    pipeline = key_handler(mouse_handler(timer_handler()))
    while True:
        event = Event.next()
        if event.kind == TERMINATE:
            break
        pipeline.send(event)

    print("\nHandler Chain #2 (debugging)")
    pipeline = debug_handler(pipeline)
    while True:
        event = Event.next()
        if event.kind == TERMINATE:
            break
        pipeline.send(event)


if __name__ == "__main__":
    main()

