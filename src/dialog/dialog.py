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
from src.lib import ui
from src.lib import util
from gettext import gettext as _


class CancelError(Exception):
    """Exception for dialog cancellations"""
    pass


class Message(Gtk.Dialog):
    """A message dialog"""

    def __init__(self, parent, title, text, stockimage, buttons=(), default=None):
        Gtk.Dialog.__init__(self, title=title, transient_for=parent.window, flags=0, modal=True,
                            destroy_with_parent=True)

        self.add_buttons(*buttons)

        box = Gtk.HBox(spacing=12)
        self.add(box)

        # set up image
        if stockimage is not None:
            pass
            # image = ui.Image(stockimage, Gtk.IconSize.DIALOG)
            # image.set_alignment(0.5, 0)
            # box.pack_start(image, False, False)

        # set up message
        self.contents = Gtk.HBox(spacing=10)
        box.pack_start(self.contents, False, False, 10)

        label = ui.Label("<span size=\"larger\" weight=\"bold\">%s</span>\n\n%s" % (util.escape_markup(title), text))
        label.set_alignment(0, 0)
        label.set_selectable(True)
        self.contents.pack_start(label, False, False, 10)

        label = Gtk.Label("This is a dialog to display additional information")
        box.add(label)

    def run(self):
        """Displays the dialog"""

        self.show_all()
        response = Gtk.Widget.run(self)
        self.destroy()

        return response


class Warning(Message):
    """Displays a warning message"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.ResponseType.OK),), default=None):
        Message.__init__(self, parent, title, text, ui.STOCK_WARNING, buttons, default)


class FileChanges(Warning):
    """Asks to save changes before proceeding"""

    def __init__(self, parent, title, text):
        Warning.__init__(
            self, parent, title, text,
            ((ui.STOCK_DISCARD, Gtk.RESPONSE_ACCEPT), (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
             (Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        )

    def run(self):
        """Displays the dialog"""

        response = Warning.run(self)

        if response == Gtk.ResponseType.OK:
            return True

        elif response == Gtk.RESPONSE_ACCEPT:
            return False

        elif response in (Gtk.ResponseType.CANCEL, Gtk.RESPONSE_CLOSE):
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

    def __init__(self, window):
        super().__init__(title=_("Please choose a revelation file"), transient_for=window,
                         action=Gtk.FileChooserAction.OPEN)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        self.set_default_size(800, 400)

        filter_text = Gtk.FileFilter()
        filter_text.set_name(_('Revelation files'))
        filter_text.add_mime_type("application/x-revelation")
        self.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name(_('All files'))
        filter_any.add_pattern("*")
        self.add_filter(filter_any)


class Error(Message):
    """Displays an error message"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.ResponseType.OK),), default=None):
        Message.__init__(self, parent, title, text, Gtk.STOCK_DIALOG_ERROR, buttons, default)


class Info(Message):
    """Displays an info message"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.ResponseType.OK),), default=None):
        Message.__init__(self, parent, title, text, Gtk.STOCK_DIALOG_INFO, buttons, default)


class Question(Message):
    """Displays a question"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.ResponseType.OK),), default=None):
        Message.__init__(self, parent, title, text, Gtk.STOCK_DIALOG_QUESTION, buttons, default)


class Warning(Message):
    """Displays a warning message"""

    def __init__(self, parent, title, text, buttons=((Gtk.STOCK_OK, Gtk.ResponseType.OK),), default=None):
        Message.__init__(self, parent, title, text, ui.STOCK_WARNING, buttons, default)


##### PASSWORD DIALOGS #####

class Password(Message):
    """A base dialog for asking for passwords"""

    def __init__(self, parent, title, text, stock=Gtk.STOCK_OK):
        Message.__init__(self, parent, title, text, Gtk.STOCK_DIALOG_AUTHENTICATION, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.entries = []

        self.sect_passwords = ui.InputSection()
        self.contents.pack_start(self.sect_passwords, False, False, 10)

    def add_entry(self, name, entry=None):
        """Adds a password entry to the dialog"""

        if entry is None:
            entry = ui.Entry()
            entry.set_visibility(False)

        self.sect_passwords.append_widget(name, entry)
        self.entries.append(entry)

        return entry

    def run(self):
        """Displays the dialog"""

        self.show_all()

        if len(self.entries) > 0:
            self.entries[0].grab_focus()

        return Gtk.Dialog.run(self)


class PasswordChange(Password):
    """A dialog for changing the password"""

    def __init__(self, parent, password=None):
        Password.__init__(
            self, parent, _('Enter new password'),
            _(
                'Enter a new password for the current data file. The file must be saved before the new password is applied.'),
            ui.STOCK_PASSWORD_CHANGE
        )

        self.password = password

        if password is not None:
            self.entry_current = self.add_entry(_('Current password'))

        self.entry_new = self.add_entry(_('New password'), ui.PasswordEntry())
        self.entry_confirm = self.add_entry(_('Confirm password'))
        self.entry_confirm.autocheck = False

    def run(self):
        """Displays the dialog"""

        while 1:
            if Password.run(self) is not Gtk.ResponseType.OK:
                self.destroy()
                raise CancelError

            elif self.password is not None and self.entry_current.get_text() is not self.password:
                Error(self, _('Incorrect password'),
                      _('The password you entered as the current file password is incorrect.')).run()

            elif self.entry_new.get_text() != self.entry_confirm.get_text():
                Error(self, _('Passwords don\'t match'),
                      _('The password and password confirmation you entered does not match.')).run()

            else:
                password = self.entry_new.get_text()

                try:
                    util.check_password(password)

                except ValueError as res:
                    response = Warning(
                        self, _('Use insecure password?'),
                        _('The password you entered is not secure; %s. Are you sure you want to use it?') % str(
                            res).lower(),
                        ((Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL), (Gtk.STOCK_OK, Gtk.ResponseType.OK)),
                        Gtk.ResponseType.CANCEL
                    ).run()

                    if response != Gtk.ResponseType.OK:
                        continue

                self.destroy()
                return password


class PasswordLock(Password):
    """Asks for a password when the file is locked"""

    def __init__(self, parent, password):
        Password.__init__(
            self, parent, _('Enter password to unlock file'),
            _('The current file has been locked, please enter the file password to unlock it.'),
            ui.STOCK_UNLOCK
        )

        self.get_button(1).set_label(Gtk.STOCK_QUIT)

        self.password = password
        self.entry_password = self.add_entry(_('Password'))

    def run(self):
        """Displays the dialog"""

        while 1:
            try:
                response = Password.run(self)

                if response == Gtk.ResponseType.CANCEL:
                    raise CancelError

                elif response != Gtk.ResponseType.OK:
                    continue

                elif self.entry_password.get_text() == self.password:
                    break

                else:
                    Error(self, _('Incorrect password'),
                          _('The password you entered was not correct, please try again.')).run()

            except CancelError:
                if self.get_button(1).get_property("sensitive") is True:
                    self.destroy()
                    raise

                else:
                    continue

        self.destroy()


class PasswordOpen(Password):
    """Password dialog for opening files"""

    def __init__(self, parent, filename):
        Password.__init__(
            self, parent, _('Enter file password'),
            _('The file \'%s\' is encrypted. Please enter the file password to open it.') % filename,
            Gtk.STOCK_OPEN
        )

        self.entry_password = self.add_entry(_('Password'))

    def run(self):
        """Displays the dialog"""

        response = Password.run(self)
        password = self.entry_password.get_text()
        self.destroy()

        if response == Gtk.ResponseType.OK:
            return password

        else:
            raise CancelError


class PasswordSave(Password):
    """Password dialog for saving data"""

    def __init__(self, parent, filename):
        Password.__init__(
            self, parent, _('Enter password for file'),
            _(
                'Please enter a password for the file \'%s\'. You will need this password to open the file at a later time.') % filename,
            Gtk.STOCK_SAVE
        )

        self.entry_new = self.add_entry(_('New password'), ui.PasswordEntry())
        self.entry_confirm = self.add_entry(_('Confirm password'))
        self.entry_confirm.autocheck = False

    def run(self):
        """Displays the dialog"""

        while 1:
            if Password.run(self) != Gtk.ResponseType.OK:
                self.destroy()
                raise CancelError

            elif self.entry_new.get_text() != self.entry_confirm.get_text():
                Error(self, _('Passwords don\'t match'), _('The passwords you entered does not match.')).run()

            elif len(self.entry_new.get_text()) == 0:
                Error(self, _('No password entered'), _('You must enter a password for the new data file.')).run()

            else:
                password = self.entry_new.get_text()

                try:
                    util.check_password(password)

                except ValueError as res:
                    res = str(res).lower()

                    response = Warning(
                        self, _('Use insecure password?'),
                        _('The password you entered is not secure; %s. Are you sure you want to use it?') % res,
                        ((Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL), (Gtk.STOCK_OK, Gtk.ResponseType.OK)),
                        Gtk.ResponseType.CANCEL
                    ).run()

                    if response != Gtk.ResponseType.OK:
                        continue

                self.destroy()
                return password
