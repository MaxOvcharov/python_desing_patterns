#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/mediator.py
Посредник (Mediator) - паттерн поведения объектов.

Определяет объект, инкапсулирующий способ взаимодействия множества объектов.
Посредник обеспечивает слабую связанность системы, избавляя объекты от
необходимости явно ссылаться друг на друга, позволяя тем самым независимо
изменять взаимодействия между ними.
"""
import abc


class WindowBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self):
        pass

    @abc.abstractmethod
    def hide(self):
        pass


class MainWindow(WindowBase):
    def show(self):
        print(f'Show {self.__class__.__name__}')

    def hide(self):
        print(f'Hide {self.__class__.__name__}')


class SettingWindow(WindowBase):
    def show(self):
        print(f'Show {self.__class__.__name__}')

    def hide(self):
        print(f'Hide {self.__class__.__name__}')


class HelpWindow(WindowBase):
    def show(self):
        print(f'Show {self.__class__.__name__}')

    def hide(self):
        print(f'Hide {self.__class__.__name__}')


class WindowMediator:
    def __init__(self):
        self.windows = dict.fromkeys(('main', 'setting', 'help'))

    def show(self, win):
        for window in self.windows.values():
            if window is not win:
                window.hide()

        win.show()

    def set_main(self, win):
        self.windows['main'] = win

    def set_setting(self, win):
        self.windows['setting'] = win

    def set_help(self, win):
        self.windows['help'] = win


def main():
    main_win = MainWindow()
    setting_win = SettingWindow()
    help_win = HelpWindow()

    med = WindowMediator()
    med.set_main(main_win)
    med.set_setting(setting_win)
    med.set_help(help_win)

    main_win.show()  # Show MainWindow

    med.show(setting_win)
    # Hide MainWindow
    # Hide HelpWindow
    # Show SettingWindow

    med.show(help_win)
    # Hide MainWindow
    # Hide SettingWindow
    # Show HelpWindow


if __name__ == '__main__':
    main()
