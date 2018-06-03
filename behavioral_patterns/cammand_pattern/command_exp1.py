#!/usr/bin/env python3
"""
EXAMPLE - https://github.com/azmikamis/pipbook/blob/master/any/grid.py
"""


class Command:

    def __init__(self, do, undo, description=""):
        assert callable(do) and callable(undo)
        self.do = do
        self.undo = undo
        self.description = description

    def __call__(self):
        self.do()


class Macro:

    def __init__(self, description=""):
        self.description = description
        self.__commands = []

    def add(self, command):
        if not isinstance(command, Command):
            raise TypeError("Expected object of type Command, got {}".
                            format(type(command).__name__))
        self.__commands.append(command)

    def __call__(self):
        for command in self.__commands:
            command()

    do = __call__

    def undo(self):
        for command in reversed(self.__commands):
            command.undo()


class Grid:

    def __init__(self, width, height):
        self.__cells = [["white" for _ in range(height)]
                        for _ in range(width)]

    def cell(self, x, y, color=None):
        if color is None:
            return self.__cells[x][y]

        self.__cells[x][y] = color

    @property
    def rows(self):
        return len(self.__cells[0])

    @property
    def columns(self):
        return len(self.__cells)

    def as_html(self, description=None):
        table = ['<table border="1" style="font-family: fixed">']
        if description is not None:
            table.append('<tr><td colspan="{}">{}</td></tr>'.format(
                self.columns, description))

        for y in range(self.rows):
            table.append("<tr>")
            for x in range(self.columns):
                color = self.__cells[x][y]
                name = color if not color.startswith("light") else color[5:]
                char = (name[0].upper() if color != "white" else
                        '<font color="white">X</font>')
                table.append('<td style="background-color: {}">{}</td>'.
                             format(color if color != "red" else "pink", char))
            table.append("</tr>")
        table.append("</table>")
        return "\n".join(table)


class UndoableGrid(Grid):

    def create_cell_command(self, x, y, color):

        def undo():
            self.cell(x, y, undo.color)

        def do():
            undo.color = self.cell(x, y) # Subtle!
            self.cell(x, y, color)

        return Command.Command(do, undo, "Cell")

    def create_rectangle_macro(self, x0, y0, x1, y1, color):
        macro = Command.Macro("Rectangle")
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                macro.add(self.create_cell_command(x, y, color))

        return macro


def main():
    html = []
    grid = UndoableGrid(8, 3)   # (1) Empty
    html.append(grid.as_html("(1) Empty"))
    red_left = grid.create_cell_command(2, 1, "red")
    red_right = grid.create_cell_command(5, 0, "red")
    red_left()                   # (2) Do Red Cells
    red_right.do()               # OR: red_right()
    html.append(grid.as_html("(2) Do Red Cells"))
    green_left = grid.create_cell_command(2, 1, "lightgreen")
    green_left()                 # (3) Do Green Cell
    html.append(grid.as_html("(3) Do Green Cell"))
    rectangle_left = grid.create_rectangle_macro(1, 1, 2, 2, "lightblue")
    rectangle_right = grid.create_rectangle_macro(5, 0, 6, 1, "lightblue")
    rectangle_left()             # (4) Do Blue Squares
    rectangle_right.do()         # OR: rectangle_right()
    html.append(grid.as_html("(4) Do Blue Squares"))
    rectangle_left.undo()        # (5) Undo Left Blue Square
    html.append(grid.as_html("(5) Undo Left Blue Square"))
    green_left.undo()            # (6) Undo Left Green Cell
    html.append(grid.as_html("(6) Undo Left Green Cell"))
    rectangle_right.undo()       # (7) Undo Right Blue Square
    html.append(grid.as_html("(7) Undo Right Blue Square"))
    red_left.undo()              # (8) Undo Red Cells
    red_right.undo()
    html.append(grid.as_html("(8) Undo Red Cells"))
    print('<table border="0"><tr><td>{}</td></tr></table>'.format(
        "</td><td>".join(html)))


if __name__ == "__main__":
    main()
