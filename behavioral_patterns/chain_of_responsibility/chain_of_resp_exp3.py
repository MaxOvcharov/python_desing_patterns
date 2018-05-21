#!/usr/bin/env python3
"""
EXAMPLE - https://github.com/azmikamis/pipbook/blob/master/any/eventhandler1.py
"""

import sys
import random
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


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, event):
        if self.__successor is not None:
            self.__successor.handle(event)


class DebugHandler(NullHandler):

    def __init__(self, successor=None, file=sys.stdout):
        super().__init__(successor)
        self.__file = file

    def handle(self, event):
        self.__file.write(f'*DEBUG*: {event}\n')
        super().handle(event)


class MouseHandler(NullHandler):

    def handle(self, event):
        if event.kind == MOUSE:
            print(f'Click:   {event}')
        else:
            super().handle(event)


class KeyHandler(NullHandler):

    def handle(self, event):
        if event.kind == KEYPRESS:
            print(f'Press:   {event}')
        else:
            super().handle(event)


class TimerHandler(NullHandler):

    def handle(self, event):
        if event.kind == TIMER:
            print(f'Timeout: {event}')
        else:
            super().handle(event)


def main():
    print("Handler Chain #1")
    handler1 = TimerHandler(KeyHandler(MouseHandler(NullHandler())))
    # Could pass None or nothing instead of the NullHandler
    while True:
        event = Event.next()
        if event.kind == TERMINATE:
            break
        handler1.handle(event)

    print("\nHandler Chain #2 (debugging)")
    handler2 = DebugHandler(handler1)
    while True:
        event = Event.next()
        if event.kind == TERMINATE:
            break
        handler2.handle(event)


if __name__ == "__main__":
    main()
