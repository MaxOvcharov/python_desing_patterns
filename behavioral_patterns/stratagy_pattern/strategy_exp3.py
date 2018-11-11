#!/usr/bin/env python3
"""
EXAMPLE - https://github.com/azmikamis/pipbook/blob/master/any/tabulator1.py.
"""
import sys
if sys.version_info[:2] < (3, 2):
    from xml.sax.saxutils import escape
else:
    from html import escape


WINNERS = (
    "Nikolai Andrianov", "Matt Biondi", "Bjørn Dæhlie",
    "Birgit Fischer", "Sawao Kato", "Larisa Latynina", "Carl Lewis",
    "Michael Phelps", "Mark Spitz", "Jenny Thompson"
)


class Layout:

    def __init__(self, tabulator):
        self.tabulator = tabulator

    def tabulate(self, rows, items):
        return self.tabulator.tabulate(rows, items)


class Tabulator:

    def tabulate(self, rows, items):
        raise NotImplementedError()


class HtmlTabulator(Tabulator):

    def tabulate(self, rows, items):
        columns, remainder = divmod(len(items), rows)
        if remainder:
            columns += 1

        column = 0
        table = ['<table border="1">\n']
        for item in items:
            if column == 0:
                table.append("<tr>")
            table.append("<td>{}</td>".format(escape(str(item))))
            column += 1
            if column == columns:
                table.append("</tr>\n")
            column %= columns

        if table[-1][-1] != "\n":
            table.append("</tr>\n")

        table.append("</table>\n")
        return "".join(table)


class TextTabulator(Tabulator):

    def tabulate(self, rows, items):
        columns, remainder = divmod(len(items), rows)
        if remainder:
            columns += 1
            remainder = (rows * columns) - len(items)
            if remainder == columns:
                remainder = 0

        column = columnWidth = 0
        for item in items:
            columnWidth = max(columnWidth, len(item))

        columnDivider = ("-" * (columnWidth + 2)) + "+"
        divider = "+" + (columnDivider * columns) + "\n"
        table = [divider]
        for item in items + (("",) * remainder):
            if column == 0:
                table.append("|")

            table.append(" {:<{}} |".format(item, columnWidth))
            column += 1
            if column == columns:
                table.append("\n")

            column %= columns

        table.append(divider)
        return "".join(table)


def main():
    htmlLayout = Layout(HtmlTabulator())
    for rows in range(2, 6):
        print(htmlLayout.tabulate(rows, WINNERS))

    textLayout = Layout(TextTabulator())
    for rows in range(2, 6):
        print(textLayout.tabulate(rows, WINNERS))


if __name__ == "__main__":
    main()
