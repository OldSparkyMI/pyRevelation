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
from gettext import gettext as _


class CancelError(Exception):
    """Exception for dialog cancellations"""
    pass


class Message(Gtk.Window):
    """A message dialog"""

    def __init__(self, parent, title, text, stockimage, buttons=(), default=None):
        Gtk.Window.__init__(self, title="MessageDialog Example")

        box = Gtk.Box(spacing=12)
        self.add(box)

        # set up image
        if stockimage != None:
            pass
            #image = ui.Image(stockimage, Gtk.IconSize.DIALOG)
            #image.set_alignment(0.5, 0)
            #box.pack_start(image, False, False)

        # set up message
        self.contents = Gtk.Box(spacing=10)
        box.pack_start(self.contents)

        #label = ui.Label("<span size=\"larger\" weight=\"bold\">%s</span>\n\n%s" % (util.escape_markup(title), text))
        #label.set_alignment(0, 0)
        #label.set_selectable(True)
        #self.contents.pack_start(label)


    def run(self):
        """Displays the dialog"""

        self.show_all()
        response = Gtk.Dialog.run(self)
        self.destroy()

        return response


class Warning(Message):
    """Displays a warning message"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.RESPONSE_OK),), default=None):
        Message.__init__(self, parent, title, text, ui.STOCK_WARNING, buttons, default)


class FileChanges(Warning):
    """Asks to save changes before proceeding"""

    def __init__(self, parent, title, text):
        Warning.__init__(
            self, parent, title, text,
            ((ui.STOCK_DISCARD, Gtk.RESPONSE_ACCEPT), (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL),
             (Gtk.STOCK_SAVE, Gtk.RESPONSE_OK))
        )

    def run(self):
        """Displays the dialog"""

        response = Warning.run(self)

        if response == Gtk.RESPONSE_OK:
            return True

        elif response == Gtk.RESPONSE_ACCEPT:
            return False

        elif response in (Gtk.RESPONSE_CANCEL, Gtk.RESPONSE_CLOSE):
            raise CancelError


class FileChangesOpen(FileChanges):
    """Asks the user to save changes when opening a different file"""

    def __init__(self, parent):
        FileChanges.__init__(
            self, parent, _('Save changes before opening?'),
            _(
                'You have made changes which have not been saved. If you open a different file without saving then these changes will be lost.')
        )


class OpenFileSelector(Gtk.FileChooserDialog):
    """A file selector for opening files"""

    def __init__(self):
        Gtk.FileChooserDialog.__init__(_("Please choose a revelation file"), self.window,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Select", Gtk.ResponseType.OK))
        self.set_default_size(800, 400)

        filter_text = Gtk.FileFilter()
        filter_text.set_name(_('Revelation files'))
        filter_text.add_mime_type("application/x-revelation")
        self.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name(_('All files'))
        filter_py.add_mime_type("*")
        self.add_filter(filter_py)
