# coding: utf-8

"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/command.py

Команда (Command, Action, Transaction) - паттерн поведения объектов.

Инкапсулирует запрос как объект, позволяя тем самым задавать параметры клиентов
для обработки соответствующих запросов, ставить запросы в очередь или протоколировать их,
а также поддерживать отмену операций.
"""
import abc

from datetime import datetime


class Light:

    @staticmethod
    def turn_on():
        print(f'Включить свет - {datetime.now()}')

    @staticmethod
    def turn_off():
        print(f'Выключить свет - {datetime.now()}')


class CommandBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self):
        pass


class LightCommandBase(CommandBase):
    def __init__(self, light):
        self.light = light


class TurnOnLightCommand(LightCommandBase):
    def execute(self):
        self.light.turn_on()


class TurnOffLightCommand(LightCommandBase):
    def execute(self):
        self.light.turn_off()


class Switch:
    def __init__(self, on_cmd, off_cmd):
        self.on_cmd = on_cmd
        self.off_cmd = off_cmd

    def on(self):
        self.on_cmd.execute()

    def off(self):
        self.off_cmd.execute()


def main():
    light = Light()
    switch = Switch(on_cmd=TurnOnLightCommand(light), off_cmd=TurnOffLightCommand(light))
    switch.on()  # Включить свет
    switch.off()  # Выключить свет


if __name__ == '__main__':
    main()

