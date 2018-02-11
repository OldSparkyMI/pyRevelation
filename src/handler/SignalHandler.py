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

class MenuHandler:
    """Sets up all toolbar actions"""

    pyRevelation = None

    def menu_file_new(self):
        print("menu_file_new")

    def menu_file_open(self):
        print("menu_file_open")

    def menu_file_save(self):
        print("menu_file_save")

    def menu_file_save_as(self):
        print("menu_file_save_as")

    def menu_file_change_password(self):
        print("menu_file_change_password")

    def menu_file_lock(self):
        print("menu_file_lock")

    def menu_file_import(self):
        print("menu_file_import")

    def menu_file_export(self):
        print("menu_file_export")

    def menu_file_close(self):
        print("menu_file_close")

    def menu_quit(self):
        Gtk.main_quit()


class ToolbarHandler:
    """Sets up all toolbar actions"""

    pyRevelation = None

    def toolbar_file_open(self, tool_button):
        print("toolbar_file_open")
        self.pyRevelation.file_open()

    def toolbar_file_save(self):
        print("toolbar_file_save")

    def toolbar_entry_add(self):
        print("toolbar_entry_add")

    def toolbar_entry_directory(self):
        print("toolbar_entry_directory")

    def toolbar_entry_goto(self):
        print("toolbar_entry_goto")

    def toolbar_entry_edit(self):
        print("toolbar_entry_edit")

    def toolbar_entry_remove(self):
        print("toolbar_entry_remove")


class SignalHandler(ToolbarHandler, MenuHandler):
    """Sets up actions"""
    pyRevelation = None

    def __init__(self, pyrevelation):
        self.pyRevelation = pyrevelation

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)