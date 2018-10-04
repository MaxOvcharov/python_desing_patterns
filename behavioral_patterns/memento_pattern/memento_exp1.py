#!/usr/bin/env python3
"""
EXAMPLE - https://sourcemaking.com/design_patterns/memento.

Capture and externalize an object's internal state so that the object
can be restored to this state later, without violating encapsulation.
"""
import pickle


class Originator:
    """
    Create a memento containing a snapshot of its current internal
    state.
    Use the memento to restore its internal state.
    """

    def __init__(self):
        self._state = None

    def set_memento(self, memento):
        previous_state = pickle.loads(memento)
        vars(self).clear()
        vars(self).update(previous_state)

    def create_memento(self):
        return pickle.dumps(vars(self))


def main():
    originator = Originator()
    print(f'ORIGINAL: {originator.__dict__}')
    memento = originator.create_memento()
    originator._state = True
    print(f'CHANGED: {originator.__dict__}')
    originator.set_memento(memento)
    print(f'PREVIOUS: {originator.__dict__}')


if __name__ == "__main__":
    main()
