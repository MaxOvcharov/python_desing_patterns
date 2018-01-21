#!/usr/bin/env python3
"""
Example from http://www.qtrac.eu/pipbook.html
"""

import abc
import os
import re
import sys
import tempfile
if sys.version_info[:2] < (3, 2):
    from xml.sax.saxutils import escape
else:
    from html import escape


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-P":  # For regression testing
        print(create_login_form(HtmlFormBuilder()))
        print(create_login_form(TkFormBuilder()))
        return

    html_filename = os.path.join(tempfile.gettempdir(), "login.html")
    html_form = create_login_form(HtmlFormBuilder())
    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(html_form)
    print("wrote", html_filename)

    tk_filename = os.path.join(tempfile.gettempdir(), "login.py")
    tk_form = create_login_form(TkFormBuilder())
    with open(tk_filename, "w", encoding="utf-8") as file:
        file.write(tk_form)
    print("wrote", tk_filename)


def create_login_form(builder):
    builder.add_title("Login")
    builder.add_label("Username", 0, 0, target="username")
    builder.add_entry("username", 0, 1)
    builder.add_label("Password", 1, 0, target="password")
    builder.add_entry("password", 1, 1, kind="password")
    builder.add_button("Login", 2, 0)
    builder.add_button("Cancel", 2, 1)
    return builder.form()


class AbstractFormBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_title(self, title):
        self.title = title

    @abc.abstractmethod
    def form(self):
        pass

    @abc.abstractmethod
    def add_label(self, text, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_entry(self, variable, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_button(self, text, row, column, **kwargs):
        pass


class HtmlFormBuilder(AbstractFormBuilder):

    def __init__(self):
        self.title = "HtmlFormBuilder"
        self.items = {}

    def add_title(self, title):
        super().add_title(escape(title))

    def add_label(self, text, row, column, **kwargs):
        frm = '<td><label for="{}">{}:</label></td>'
        self.items[(row, column)] = (frm.format(kwargs["target"], escape(text)))

    def add_entry(self, variable, row, column, **kwargs):
        frm = """<td><input name="{}" type="{}" /></td>"""
        html = frm.format(variable, kwargs.get("kind", "text"))
        self.items[(row, column)] = html

    def add_button(self, text, row, column, **kwargs):
        frm = """<td><input type="submit" value="{}" /></td>"""
        html = frm.format(escape(text))
        self.items[(row, column)] = html

    def form(self):
        frm = "<!doctype html>\n<html><head><title>{}</title></head><body>"
        html = [frm.format(self.title), '<form><table border="0">']
        this_row = None
        for key, value in sorted(self.items.items()):
            row, column = key
            if this_row is None:
                html.append("  <tr>")
            elif this_row != row:
                html.append("  </tr>\n  <tr>")
            this_row = row
            html.append("    " + value)
        html.append("  </tr>\n</table></form></body></html>")
        return "\n".join(html)


class TkFormBuilder(AbstractFormBuilder):

    TEMPLATE = """#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk

class {name}Form(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.withdraw()     # hide until ready to show
        self.title("{title}")
        {statements}
        self.bind("<Escape>", lambda *args: self.destroy())
        self.deiconify()    # show when widgets are created and laid out
        if self.winfo_viewable():
            self.transient(master)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

if __name__ == "__main__":
    application = tk.Tk()
    window = {name}Form(application)
    application.protocol("WM_DELETE_WINDOW", application.quit)
    application.mainloop()
"""

    def __init__(self):
        self.title = "TkFormBuilder"
        self.statements = []

    def add_title(self, title):
        super().add_title(title)

    def add_label(self, text, row, column, **kwargs):
        frm1 = """self.{}Label = ttk.Label(self, text="{}:")"""
        name = self._canonicalize(text)
        create = frm1.format(name, text)
        frm2 = """self.{}Label.grid(row={}, column={}, sticky=tk.W, 
        padx="0.75m", pady="0.75m")"""
        layout = frm2.format(name, row, column)
        self.statements.extend((create, layout))

    def add_entry(self, variable, row, column, **kwargs):
        name = self._canonicalize(variable)
        extra = "" if kwargs.get("kind") != "password" else ', show="*"'
        create = "self.{}Entry = ttk.Entry(self{})".format(name, extra)
        frm = """self.{}Entry.grid(row={}, column={}, sticky=(tk.W, tk.E),
         padx="0.75m", pady="0.75m")"""
        layout = frm.format(name, row, column)
        self.statements.extend((create, layout))

    def add_button(self, text, row, column, **kwargs):
        name = self._canonicalize(text)
        frm1 = """self.{}Button = ttk.Button(self, text="{}")"""
        create = (frm1.format(name, text))
        frm2 = """self.{}Button.grid(row={}, column={}, padx="0.75m", 
        pady="0.75m")"""
        layout = frm2.format(name, row, column)
        self.statements.extend((create, layout))

    def form(self):
        return TkFormBuilder.\
            TEMPLATE.format(title=self.title,
                            name=self._canonicalize(self.title, False),
                            statements="\n        ".join(self.statements))

    def _canonicalize(self, text, start_lower=True):
        text = re.sub(r"\W+", "", text)
        if text[0].isdigit():
            return "_" + text
        return text if not start_lower else text[0].lower() + text[1:]


if __name__ == "__main__":
    main()
