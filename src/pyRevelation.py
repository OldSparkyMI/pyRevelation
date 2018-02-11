#!/usr/bin/python

#
# Revelation - a password manager for GNOME
# https://github.com/OldSparkyMI/pyRevelation
# $Id$
#
# Copyright (c) 2018 Maik Igloffstein
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.handler.SignalHandler import SignalHandler
from gettext import gettext as _
import sys


# TODO: One last thing. It's important to understand that Python's gettext module only handles Python strings, and other subsystems may be involved. The classic example is GObject Introspection, the newest and recommended interface to the GNOME Object system. If your Python-GI based project needs to translate strings too (e.g. in menus or other UI elements), you'll have to use both the gettext API for your Python strings, and set the locale for the C-based bits using locale.setlocale(). This is because Python's API does not set the locale automatically, and Python-GI exposes no other way to control the language it uses for translations.

class PyRevelationApplication(Gtk.Application):
    """The Revelation application"""

    builder = None
    window = None

    # constructor of the Gtk Application
    def __init__(self):
        Gtk.Application.__init__(self)

    # loads the glade file
    def do_activate(self):
        self.window = self.get_window()
        self.window.show()
        Gtk.main()

    def get_window(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../data/glade/pyRevelation.glade")
        self.builder.connect_signals(SignalHandler(self))
        return self.builder.get_object("PyRevelationApplicationWindow")

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)

    def file_open(self):
        print("file_open")
        dialog = Gtk.FileChooserDialog(_("Please choose a folder"), self.window,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    # def add_filters(self, dialog):
    #     filter_text = Gtk.FileFilter()
    #     filter_text.set_name("Text files")
    #     filter_text.add_mime_type("text/plain")
    #     dialog.add_filter(filter_text)
    #
    #     filter_py = Gtk.FileFilter()
    #     filter_py.set_name("Python files")
    #     filter_py.add_mime_type("text/x-python")
    #     dialog.add_filter(filter_py)
    #
    #     filter_any = Gtk.FileFilter()
    #     filter_any.set_name("Any files")
    #     filter_any.add_pattern("*")
    #     dialog.add_filter(filter_any)


if __name__ == "__main__":
    app = PyRevelationApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
