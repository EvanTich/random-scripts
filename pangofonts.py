#!/usr/bin/env python3
# Tells you the system fonts that Pango recognizes. Had to use
#  it to find a font identifier one time. Completely stolen
#  from some other place, but it was useful.

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Example(Gtk.Window):
    """Using Pango to get system fonts names"""

    def list_system_fonts(self):
        """Yield system fonts families names using Pango"""
        context = self.create_pango_context()
        for fam in context.list_families():
            yield fam.get_name()


a = Example()
system_fonts = list(a.list_system_fonts())
print(system_fonts)
