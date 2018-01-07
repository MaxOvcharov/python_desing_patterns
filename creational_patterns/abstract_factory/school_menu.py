#!/usr/bin/env python3
# coding: utf-8
"""
Абстрактная фабрика (Abstract factory, Kit) - паттерн, порождающий объекты.
Предоставляет интерфейс для создания семейств взаимосвязанных или взаимозависимых объектов,
не специфицируя их конкретных классов.
Классы абстрактной фабрики часто реализуются фабричными методами,
но могут быть реализованы и с помощью паттерна прототип.
"""
import calendar

from collections import namedtuple
from datetime import datetime


class BreakfastFactory:

    @classmethod
    def create_drink(cls, date):
        return cls.Drink(date)

    @classmethod
    def create_food(cls, date):
        return cls.Food(date)

    class Drink:

        DRINKS = {
            'Monday': 'milk',
            'Tuesday': 'juice',
            'Wednesday': 'milk',
            'Thursday': 'juice',
            'Friday': 'juice',
            'Saturday': 'WEEKEND DAY',
            'Sunday': 'WEEKEND DAY'
        }

        def __init__(self, date):
            self._wd_name = _convert_date(date)
            self._drink_name = \
                self.DRINKS[self._wd_name] if self._wd_name in self.DRINKS else None

        def __str__(self):
            return f'{self._wd_name}: Drink - {self._drink_name}'

    class Food(object):

        FOODS = {
            'Monday': 'porridge',
            'Tuesday': 'scrambled eggs',
            'Wednesday': 'porridge',
            'Thursday': 'scrambled eggs',
            'Friday': 'cheeseburger',
            'Saturday': 'WEEKEND DAY',
            'Sunday': 'WEEKEND DAY'
        }

        def __init__(self, date):
            self._wd_name = _convert_date(date)
            self._food_name = \
                self.FOODS[self._wd_name] if self._wd_name in self.FOODS else None

        def __str__(self):
            return f'{self._wd_name}: Food - {self._food_name}'


class LunchFactory(BreakfastFactory):

    class Drink:

        DRINKS = {
            'Monday': 'tea',
            'Tuesday': 'coffee',
            'Wednesday': 'tea',
            'Thursday': 'juice',
            'Friday': 'juice',
            'Saturday': 'WEEKEND DAY',
            'Sunday': 'WEEKEND DAY'
        }

        def __init__(self, date):
            self._wd_name = _convert_date(date)
            self._drink_name = \
                self.DRINKS[self._wd_name] if self._wd_name in self.DRINKS else None

        def __str__(self):
            return f'{self._wd_name}: Drink - {self._drink_name}'

    class Food(object):

        FOODS = {
            'Monday': 'onion soup',
            'Tuesday': 'Mushroom cream soup',
            'Wednesday': 'fried rice with sausage',
            'Thursday': 'Mushroom cream soup',
            'Friday': 'fried rice with sausage',
            'Saturday': 'WEEKEND DAY',
            'Sunday': 'WEEKEND DAY'
        }

        def __init__(self, date):
            self._wd_name = _convert_date(date)
            self._food_name = \
                self.FOODS[self._wd_name] if self._wd_name in self.FOODS else None

        def __str__(self):
            return f'{self._wd_name}: Food - {self._food_name}'


def _convert_date(date):
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, '%d.%m.%Y')
        weekday_name = calendar.day_name[date.weekday()]
    except ValueError:
        weekday_name = 'WRONG DATE FORMAT(d.m.y)'

    return weekday_name


def create_menu(factory, date=None):
    Menu = namedtuple('Menu', ['drink', 'food'])
    date = datetime.today() if date is None else date
    drink = factory.create_drink(date)
    food = factory.create_food(date)
    return Menu(drink=drink, food=food)


def main():
    breakfast_menu = create_menu(BreakfastFactory, date='12/12/1990')
    lunch_menu = create_menu(LunchFactory)
    print(f'BREAKFAST: 1) {breakfast_menu.drink}, 2) {breakfast_menu.food}')
    print(f'LUNCH: 1) {lunch_menu.drink}, 2) {lunch_menu.food}')


if __name__ == "__main__":
    main()
