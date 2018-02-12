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

#
# Module for basic datahandler functionality
#


class Error(Exception):
    """Base exception for data handler"""
    pass


class DataError(Error):
    """Exception for invalid data"""
    pass


class FormatError(Error):
    """Exception for invalid file formats"""
    pass


class PasswordError(Error):
    """Exception for wrong password"""
    pass


class VersionError(Error):
    """Exception for unknown versions"""
    pass


class DataHandler(object):
    """A datahandler base class, real datahandlers are subclassed from this"""

    name = None
    importer = False
    exporter = False
    encryption = False

    def __init__(self):
        pass

    def check(self, input):
        """Fallback method, subclasses should override this"""

        pass

    def detect(self, input):
        """Fallback method, subclasses should override this"""

        return False

    def export_data(self, entrystore, password):
        """Fallback method, subclasses should override this"""

        return ""

    def import_data(self, input, password):
        """Fallback method, subclasses should override this"""

        pass
