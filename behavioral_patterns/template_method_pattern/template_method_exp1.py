#!/usr/bin/env python3
"""
EXAMPLE - https://sourcemaking.com/design_patterns/template_method.

Define the skeleton of an algorithm in an operation, deferring some
steps to subclasses. Template Method lets subclasses redefine certain
steps of an algorithm without changing the algorithm's structure.
"""
import abc


class AbstractClass(metaclass=abc.ABCMeta):
    """
    Define abstract primitive operations that concrete subclasses define
    to implement steps of an algorithm.
    Implement a template method defining the skeleton of an algorithm.
    The template method calls primitive operations as well as operations
    defined in AbstractClass or those of other objects.
    """

    def template_method(self):
        self._primitive_operation_1()
        self._primitive_operation_2()

    @abc.abstractmethod
    def _primitive_operation_1(self):
        pass

    @abc.abstractmethod
    def _primitive_operation_2(self):
        pass


class ConcreteClass(AbstractClass):
    """
    Implement the primitive operations to carry out
    subclass-specificsteps of the algorithm.
    """

    def _primitive_operation_1(self):
        print(f'OPERATOR_1: {ConcreteClass}')

    def _primitive_operation_2(self):
        print(f'OPERATOR_2: {ConcreteClass}')


def main():
    concrete_class = ConcreteClass()
    concrete_class.template_method()


if __name__ == "__main__":
    main()