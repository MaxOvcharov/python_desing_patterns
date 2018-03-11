# coding: utf-8

"""
EXAMPLE - https://pypi.python.org/pypi/singleton-decorator/1.0.0

A testable singleton decorator allows easily create a singleton
  objects just adding a decorator to class definition but also
  allows easily write unit tests for those classes.
"""


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class MyClass(object):

    def __init__(self, name):
        """ Example class. """
        self.name = name

    def get_name(self):
        return self.name


def main():
    m1 = MyClass('Test_singleton_1')
    print(f"Create instance: {m1.get_name()}")
    m2 = MyClass('Test_singleton_2')
    print(f"Create instance: {m2.get_name()}")

    print(f"Check SINGLETON: {m1 is m2}")


if __name__ == "__main__":
    main()
