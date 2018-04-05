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
from src.dialog import dialog
from src.lib import data
from src.lib import config
from src.lib import entry
from src.lib import io
from src import datahandler
from src.lib import ui
import sys
import os


# TODO: One last thing. It's important to understand that Python's gettext module only handles Python strings, and other subsystems may be involved. The classic example is GObject Introspection, the newest and recommended interface to the GNOME Object system. If your Python-GI based project needs to translate strings too (e.g. in menus or other UI elements), you'll have to use both the gettext API for your Python strings, and set the locale for the C-based bits using locale.setlocale(). This is because Python's API does not set the locale automatically, and Python-GI exposes no other way to control the language it uses for translations.

class PyRevelationApplication(Gtk.Application):
    """The Revelation application"""

    builder = None
    window = None

    # constructor of the Gtk Application
    def __init__(self):
        self.__init_facilities()
        Gtk.Application.__init__(self)

    def __init_pyRevelationApplication(self):
        self.statusbar = self.builder.get_object('statusbar1')  # Gtk.Statusbar
        self.statusbar.__class__ = ui.Statusbar                 # cast to ui.Statusbar
        self.statusbar.__init__()                               # run init, to initialize the context

    def __init_facilities(self):
        """Sets up various facilities"""

        self.clipboard = data.Clipboard()
        self.config = config.Config()
        self.datafile = io.DataFile(datahandler.Revelation2)
        self.entryclipboard = data.EntryClipboard()
        self.entrystore = data.EntryStore()
        self.entrysearch = data.EntrySearch(self.entrystore)
        self.items = ui.ItemFactory(self)
        self.locktimer = data.Timer()
        self.undoqueue = data.UndoQueue()

        # ToDo: fixme
        # self.datafile.connect("changed", lambda w, f: self.__state_file(f))
        # self.datafile.connect("content-changed", self.__cb_file_content_changed)
        # self.entryclipboard.connect("content-toggled", lambda w, d: self.__state_clipboard(d))
        # self.locktimer.connect("ring", self.__cb_file_autolock)
        # self.undoqueue.connect("changed", lambda w: self.__state_undo(self.undoqueue.get_undo_action(),
        #                                                               self.undoqueue.get_redo_action()))

        # check if configuration is updated, install schema if not
        # if self.__check_config() == False:
        #
        #     if config.install_schema("%s/revelation.schemas" % config.DIR_GCONFSCHEMAS) == False:
        #         raise config.ConfigError
        #
        #     self.config.client.clear_cache()
        #
        #     if self.__check_config() == False:
        #         raise config.ConfigError
        #
        # self.config.monitor("file/autolock_timeout", lambda k, v, d: self.locktimer.start(v * 60))
        #
        # dialog.EVENT_FILTER = self.__cb_event_filter

    # loads the glade file
    def do_activate(self):
        self.window = self.get_window()
        self.window.show()
        Gtk.main()

    def get_window(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../data/glade/pyRevelation.glade")
        self.builder.connect_signals(SignalHandler(self))

        self.__init_pyRevelationApplication()

        return self.builder.get_object("PyRevelationApplicationWindow")

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)

    def file_open(self, file=None, password=None):
        """Opens a data file"""

        try:
            if self.entrystore.changed and dialog.FileChangesOpen(self).run():
                if not self.file_save(self.datafile.get_file(), self.datafile.get_password()):
                    raise dialog.CancelError

            if file is None:
                open_file_selector_dialog = dialog.OpenFileSelector(self.window)
                response = open_file_selector_dialog.run()
                if response == Gtk.ResponseType.OK:
                    file = open_file_selector_dialog.get_filename()
                elif response == Gtk.ResponseType.CANCEL:
                    pass
                open_file_selector_dialog.destroy()

            entrystore = self.__file_load(file, password)

            if entrystore is None:
                return

            self.entrystore.clear()
            self.entrystore.import_entry(entrystore, None)
            self.entrystore.changed = False
            self.undoqueue.clear()

            self.file_locked = False
            self.statusbar.set_status(_('Opened file %s') % self.datafile.get_file())

        except dialog.CancelError:
            self.statusbar.set_status(_('Open cancelled'))

    def __file_load(self, file, password, datafile=None):
        """Loads data from a data file into an entrystore"""

        # We may need to change the datahandler
        old_handler = None

        try:
            if datafile is None:
                datafile = self.datafile

                # Because there are two fileversion we need to check if we are really dealing
                # with version two. (This is deprecated)<<< The chances are low, that we are
                # dealing with version one. In this case we use the version one
                # handler and save the file as version two if it is changed, to
                # allow seemless upgrades.>>>
                if datafile.get_handler().detect(io.file_read(file)) is not True:
                    # Store the datahandler to be reset later on
                    old_handler = datafile.get_handler()
                    # Load the revelation fileversion one handler
                    datafile.set_handler(datahandler.Revelation)
                    dialog.Info(self, _('Old file format'), _(
                        'Revelation detected that \'%s\' file has the old and actually non-secure file format. It is '
                        'strongly recommended to save this file with the new format. Revelation will do it '
                        'automatically if you press save after opening the file.') % file).run()

            while 1:
                try:
                    result = datafile.load(file, password,
                                           lambda: dialog.PasswordOpen(self, os.path.basename(file)).run())
                    break

                except datahandler.PasswordError:
                    dialog.Error(self, _('Incorrect password'),
                                 _('The password you entered for the file \'%s\' was not correct.') % file).run()

        except datahandler.FormatError:
            self.statusbar.set_status(_('Open failed'))
            dialog.Error(self, _('Invalid file format'), _('The file \'%s\' contains invalid data.') % file).run()

        except (datahandler.DataError, entry.EntryTypeError, entry.EntryFieldError):
            self.statusbar.set_status(_('Open failed'))
            dialog.Error(self, _('Unknown data'), _(
                'The file \'%s\' contains unknown data. It may have been created by a newer version of Revelation.')
                         % file).run()

        except datahandler.VersionError:
            self.statusbar.set_status(_('Open failed'))
            dialog.Error(self, _('Unknown data version'), _(
                'The file \'%s\' has a future version number, please upgrade Revelation to open it.') % file).run()

        except datahandler.DetectError:
            self.statusbar.set_status(_('Open failed'))
            dialog.Error(self, _('Unable to detect filetype'), _(
                'The file type of the file \'%s\' could not be automatically detected. Try specifying the file type '
                'manually.') % file).run()

        except IOError:
            self.statusbar.set_status(_('Open failed'))
            dialog.Error(self, _('Unable to open file'), _(
                'The file \'%s\' could not be opened. Make sure that the file exists, and that you have permissions '
                'to open it.') % file).run()

        # If we switched the datahandlers before we need to switch back to the
        # version2 handler here, to ensure a seemless version upgrade on save
        if old_handler is not None:
            datafile.set_handler(old_handler.__class__)

        return result


if __name__ == "__main__":
    app = PyRevelationApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
