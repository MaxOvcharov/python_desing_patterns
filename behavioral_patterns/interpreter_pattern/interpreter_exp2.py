#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/interpreter.py
Интерпретатор (Interpreter) - паттерн поведения классов.

Для заданного языка определяет представление его грамматики,
а также интерпретатор предложений этого языка.
"""


class RomanNumeralInterpreter():
    """Интерпретатор римских цифр"""

    def __init__(self):
        self.grammar = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

    def interpret(self, text):
        numbers = list(map(self.grammar.get, text))  # строки в значения
        if None in numbers:
            raise ValueError(f'Ошибочное значение: {text}')
        result = 0  # накапливаем результат
        temp = None  # запоминаем последнее значение
        while numbers:
            num = numbers.pop(0)
            result += num if temp is None or temp >= num else (num - temp * 2)
            temp = num

        return result


def main():
    interp = RomanNumeralInterpreter()
    print('RESULT_1 (MMMCMXCIX = 3999) -> {}'.format(interp.interpret('MMMCMXCIX') == 3999))
    print('RESULT_2 (MCMLXXXVIII = 1988) -> {}'.format(interp.interpret('MCMLXXXVIII') == 1988))


if __name__ == "__main__":
    main()
