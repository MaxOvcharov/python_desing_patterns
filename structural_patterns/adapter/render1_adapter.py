#!/usr/bin/env python3
"""
Example from http://www.qtrac.eu/pipbook.html
Адаптер - паттерн, структурирующий классы и объекты.

Преобразует интерфейс одного класса в интерфейс другого,
  который ожидают клиенты. Адаптер обеспечивает совместную
  работу классов с несовместимыми интерфейсами, которая
  без него была бы невозможна.
"""

import abc
import collections
import sys
import textwrap
if sys.version_info[:2] < (3, 2):
    from xml.sax.saxutils import escape
else:
    from html import escape

if sys.version_info[:2] >= (3, 3):
    class Renderer(metaclass=abc.ABCMeta):

        @classmethod
        def __subclasshook__(cls, subcls):
            if cls is Renderer:
                attributes = collections.ChainMap(
                    *(Superclass.__dict__ for Superclass in subcls.__mro__)
                )

                methods = ("header", "paragraph", "footer")
                if all(method in attributes for method in methods):
                    return True

            return NotImplemented
else:
    class Renderer(metaclass=abc.ABCMeta):

        @classmethod
        def __subclasshook__(cls, subcls):
            if cls is Renderer:
                needed = {"header", "paragraph", "footer"}
                for Superclass in subcls.__mro__:
                    for meth in needed.copy():
                        if meth in Superclass.__dict__:
                            needed.discard(meth)

                    if not needed:
                        return True

            return NotImplemented


MESSAGE = "This is a very short {} paragraph that " \
          "demonstrates the simple {} class."


class Page:

    def __init__(self, title, renderer):
        if not isinstance(renderer, Renderer):
            err_msg = "Expected object of type Renderer, got {}"
            raise TypeError(err_msg.format(type(renderer).__name__))
        self.title = title
        self.renderer = renderer
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def render(self):
        self.renderer.header(self.title)
        for paragraph in self.paragraphs:
            self.renderer.paragraph(paragraph)

        self.renderer.footer()


class TextRenderer:

    def __init__(self, width=80, file=sys.stdout):
        self.width = width
        self.file = file
        self.previous = False

    def header(self, title):
        fmt = "{0:^{2}}\n{1:^{2}}\n"
        self.file.write(fmt.format(title, "=" * len(title), self.width))

    def paragraph(self, text):
        if self.previous:
            self.file.write("\n")
        self.file.write(textwrap.fill(text, self.width))
        self.file.write("\n")
        self.previous = True

    def footer(self):
        pass


class HtmlRenderer:

    def __init__(self, html_writer):
        self.htmlWriter = html_writer

    def header(self, title):
        self.htmlWriter.header()
        self.htmlWriter.title(title)
        self.htmlWriter.start_body()

    def paragraph(self, text):
        self.htmlWriter.body(text)

    def footer(self):
        self.htmlWriter.end_body()
        self.htmlWriter.footer()


class HtmlWriter:

    def __init__(self, file=sys.stdout):
        self.file = file

    def header(self):
        self.file.write("<!doctype html>\n<html>\n")

    def title(self, title):
        fmt = "<head><title>{}</title></head>\n"
        self.file.write(fmt.format(escape(title)))

    def start_body(self):
        self.file.write("<body>\n")

    def body(self, text):
        self.file.write("<p>{}</p>\n".format(escape(text)))

    def end_body(self):
        self.file.write("</body>\n")

    def footer(self):
        self.file.write("</html>\n")


def main():
    paragraph1 = MESSAGE.format("plain-text", "TextRenderer")
    paragraph2 = "This is another short paragraph just so that " \
                 "we can see two paragraphs in action."
    title = "Plain Text"

    text_page = Page(title, TextRenderer(22))
    text_page.add_paragraph(paragraph1)
    text_page.add_paragraph(paragraph2)
    text_page.render()

    print()

    paragraph1 = MESSAGE.format("HTML", "HtmlRenderer")
    title = "HTML"
    file = sys.stdout
    html_page = Page(title, HtmlRenderer(HtmlWriter(file)))
    html_page.add_paragraph(paragraph1)
    html_page.add_paragraph(paragraph2)
    html_page.render()

    try:
        page = Page(title, HtmlWriter())
        page.render()
        print("ERROR! rendering with an invalid renderer")
    except TypeError as err:
        print(err)


if __name__ == "__main__":
    main()
