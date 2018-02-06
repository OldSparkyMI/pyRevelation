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
from gi.repository import Gdk
from gi.repository import Gio
import sys


class SignalHandler:
    """Sets up actions"""

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    # callback function connected to the signal "clicked" of the button "open"
    def do_clicked(self):
        print("You clicked me!")


class PyRevelationApplication(Gtk.Application):
    """The Revelation application"""
    # constructor of the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)

    # loads the glade file
    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file("../data/glade/pyRevelation.glade")
        builder.connect_signals(SignalHandler)

        window = builder.get_object("PyRevelationApplicationWindow")
        window.show()

        Gtk.main()

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)


if __name__ == "__main__":
    app = PyRevelationApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
