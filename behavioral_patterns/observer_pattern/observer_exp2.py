#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/observer.py.

Наблюдатель (Observer, Dependents, Publish-Subscribe) - паттерн поведения объектов.
Определяет зависимость типа "один ко многим" между объектами таким образом,
что при изменении состояния одного объекта все зависящие от него оповещаются об этом
и автоматически обновляются.
"""


class Subject:
    """Субъект"""
    def __init__(self):
        self._data = None
        self._observers = set()

    def attach(self, observer):
        # подписаться на оповещение
        if not isinstance(observer, ObserverBase):
            raise TypeError()
        self._observers.add(observer)

    def detach(self, observer):
        # отписаться от оповещения
        self._observers.remove(observer)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        self.notify(data)

    def notify(self, data):
        # уведомить всех наблюдателей о событии
        for observer in self._observers:
            observer.update(data)


class ObserverBase(object):
    """Абстрактный наблюдатель"""
    def update(self, data):
        raise NotImplementedError()


class Observer(ObserverBase):
    """Наблюдатель"""
    def __init__(self, name):
        self._name = name

    def update(self, data):
        print(f'{self._name}: {data}')


def main():
    subject = Subject()
    subject.attach(Observer('Наблюдатель 1'))
    subject.attach(Observer('Наблюдатель 2'))
    subject.set_data('данные для наблюдателя')
    # Наблюдатель 2: данные для наблюдателя
    # Наблюдатель 1: данные для наблюдателя


if __name__ == "__main__":
    main()
