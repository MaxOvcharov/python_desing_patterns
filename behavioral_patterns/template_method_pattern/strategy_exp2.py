#!/usr/bin/env python3
# coding: utf-8
"""
EXAMPLE - https://github.com/pkolt/design_patterns/blob/master/behavior/strategy.py.

Стратегия (Strategy) - паттерн поведения объектов.
Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.
Стратегия позволяет изменять алгоритмы независимо от клиентов, которые ими пользуются.
"""
import abc


class ImageDecoder(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def decode(filename):
        pass


class PNGImageDecoder(ImageDecoder):
    @staticmethod
    def decode(filename):
        print(f'PNG decode: {PNGImageDecoder.__class__.__name__}')
        return PNGImageDecoder.__class__.__name__


class JPEGImageDecoder(ImageDecoder):
    @staticmethod
    def decode(filename):
        print(f'JPEG decode: {JPEGImageDecoder.__class__.__name__}')
        return JPEGImageDecoder.__class__.__name__


class GIFImageDecoder(ImageDecoder):
    @staticmethod
    def decode(filename):
        print(f'GIF decode: {GIFImageDecoder.__class__.__name__}')
        return GIFImageDecoder.__class__.__name__


class Image(object):

    @classmethod
    def open(cls, filename):
        ext = filename.rsplit('.', 1)[-1]
        if ext == 'png':
            decoder = PNGImageDecoder
        elif ext in ('jpg', 'jpeg'):
            decoder = JPEGImageDecoder
        elif ext == 'gif':
            decoder = GIFImageDecoder
        else:
            raise RuntimeError('Невозможно декодировать файл %s' % filename)

        byte_range = decoder.decode(filename)
        return cls(byte_range, filename)

    def __init__(self, byte_range, filename):
        self._byte_range = byte_range
        self._filename = filename


def main():
    Image.open('picture.png')   # PNG decode
    Image.open('picture.jpg')   # JPEG decode
    Image.open('picture.gif')   # GIF decode
    Image.open('picture.tiff')  # TIFF decode


if __name__ == '__main__':
    main()
