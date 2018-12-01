#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/template_method.py.

Шаблонный метод (Template method) - паттерн поведения классов.
Шаблонный метод определяет основу алгоритма и позволяет подклассам
переопределить некоторые шаги алгоритма, не изменяя его структуру в целом.
"""
import abc


class ExampleBase(metaclass=abc.ABCMeta):
    def template_method(self):
        self.step_one()
        self.step_two()
        self.step_three()

    @abc.abstractmethod
    def step_one(self):
        pass

    @abc.abstractmethod
    def step_two(self):
        pass

    @abc.abstractmethod
    def step_three(self):
        pass


class Example(ExampleBase):
    def step_one(self):
        print('Первый шаг алгоритма')

    def step_two(self):
        print('Второй шаг алгоритма')

    def step_three(self):
        print('Третий шаг алгоритма')


def main():
    example = Example()
    example.template_method()

    # Первый шаг алгоритма
    # Второй шаг алгоритма
    # Третий шаг алгоритма


if __name__ == '__main__':
    main()
