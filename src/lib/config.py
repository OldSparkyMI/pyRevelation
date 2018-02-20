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

import gettext
import os
import gi

gi.require_version('GConf', '2.0')
from gi.repository import GConf

from src.lib import util

_ = gettext.gettext

DIR_GConfSCHEMAS = "@pkgschemadir@"
DIR_ICONS = "@datadir@/icons"
DIR_LOCALE = "@datadir@/locale"
DIR_UI = "@pkgdatadir@/ui"

FILE_GConfTOOL = "@GConfTOOL@"

APPNAME = "revelation"
PACKAGE = "@PACKAGE@"
VERSION = "@VERSION@"
DATAVERSION = 2
RELNAME = "One Toke Over the Line"
URL = "http://revelation.olasagasti.info/"
AUTHORS = ["Maik Igloffstein <m.igloffstein@gmail.com", "Erik Grinaker <erikg@codepoet.no>",
           "Mikel Olasagasti Uranga <mikel@olasagasti.info>"]
ARTISTS = ["Erik Grinaker <erikg@codepoet.no>"]
COPYRIGHT = _(
    'Copyright') + " \302\251 2018 Maik Igloffstein\n2003-2007 Erik Grinaker\n2010-2012 Mikel Olasagasti Uranga"
LICENSE = _("""pyRevelation is free software; you can redistribute it and/or
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.""")


class ConfigError(Exception):
    """Configuration error exception"""
    pass


class Config(object):
    """Configuration class"""

    def __init__(self, basedir="/apps/revelation"):
        self.basedir = basedir
        self.client = GConf.Client.get_default()
        self.callbacks = {}

        self.client.add_dir(self.basedir, GConf.ClientPreloadType.PRELOAD_NONE)

    def __cb_notify(self, client, id, entry, data):
        """Callback for handling GConf notifications"""

        value = entry.get_value()

        if value is None:
            return

        elif value.type == GConf.VALUE_STRING:
            v = value.get_string()

        elif value.type == GConf.VALUE_BOOL:
            v = value.get_bool()

        elif value.type == GConf.VALUE_INT:
            v = value.get_int()

        # look up and call the callback
        if self.callbacks in id is False:
            raise ConfigError

        callback, userdata = self.callbacks[id]
        callback(entry.get_key(), v, userdata)

    def __resolve_keypath(self, key):
        """Resolves a key path"""

        return key[0] == "/" and key or self.basedir + "/" + key

    def forget(self, id):
        """Forgets a monitored key"""

        if self.callbacks not in id:
            raise ConfigError

        self.client.notify_remove(id)
        del self.callbacks[id]

    def get(self, key):
        """Looks up a config value"""

        value = self.client.get(self.__resolve_keypath(key))

        if value is None:
            raise ConfigError

        elif value.type == GConf.VALUE_STRING:
            return str(value.get_string())

        elif value.type == GConf.VALUE_INT:
            return value.get_int()

        elif value.type == GConf.VALUE_BOOL:
            return value.get_bool()

    def monitor(self, key, callback, userdata=None):
        "Monitor a config key for changes"

        key = self.__resolve_keypath(key)

        id = self.client.notify_add(key, self.__cb_notify)
        self.callbacks[id] = (callback, userdata)

        # call the callback to set an initial state
        callback(key, self.get(key), userdata)

        return id

    def set(self, key, value):
        "Sets a configuration value"

        node = self.client.get(self.__resolve_keypath(key))

        if node is None:
            raise ConfigError

        elif node.type == GConf.VALUE_STRING:
            node.set_string(value)

        elif node.type == GConf.VALUE_BOOL:
            node.set_bool(value)

        elif node.type == GConf.VALUE_INT:
            node.set_int(int(value))

        self.client.set(self.__resolve_keypath(key), node)

    def set_force(self, key, value):
        "Sets a value directly, ignoring if it already exists"

        key = self.__resolve_keypath(key)

        if type(value) == str:
            self.client.set_string(key, value)

        elif type(value) == bool:
            self.client.set_bool(key, value)

        elif type(value) == int:
            self.client.set_int(key, value)


def install_schema(file):
    "Installs a GConf schema"

    if os.access(file, os.F_OK) == False:
        return False

    output, status = util.execute(FILE_GConfTOOL + " --install-schema-file=" + file)

    return status == 0
