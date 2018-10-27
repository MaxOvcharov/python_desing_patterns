#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/state.py.

Состояние (State) - паттерн поведения объектов.
Позволяет объекту варьировать свое поведение в зависимости от внутреннего состояния.
Извне создается впечатление, что изменился класс объекта.
"""
import abc


class LampStateBase(metaclass=abc.ABCMeta):
    """Состояние лампы"""

    @abc.abstractmethod
    def get_color(self):
        pass


class GreenLampState(LampStateBase):
    def get_color(self):
        return 'Green'


class RedLampState(LampStateBase):
    def get_color(self):
        return 'Red'


class BlueLampState(LampStateBase):
    def get_color(self):
        return 'Blue'


class Lamp:

    def __init__(self):
        self._current_state = None
        self._states = self.get_states()

    def get_states(self):
        return [GreenLampState(), RedLampState(), BlueLampState()]

    def next_state(self):
        if self._current_state is None:
            self._current_state = self._states[0]
        else:
            index = self._states.index(self._current_state)
            if index < len(self._states) - 1:
                index += 1
            else:
                index = 0

            self._current_state = self._states[index]

        return self._current_state

    def light(self):
        state = self.next_state()
        print(state.get_color())


def main():
    lamp = Lamp()
    [lamp.light() for _ in range(3)]
    # Green
    # Red
    # Blue
    [lamp.light() for _ in range(3)]
    # Green
    # Red
    # Blue


if __name__ == "__main__":
    main()
