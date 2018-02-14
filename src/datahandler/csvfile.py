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
# Original file from: Gergely Nagy <greg@gnome.hu>
#
from src.datahandler import base
# ToDo: data is not used?
from src.lib import data, entry

import time
import csv
from io import StringIO


class CSV(base.DataHandler):
    """Data handler for CSV files"""

    name = "Comma Separated Values (CSV)"
    importer = False
    exporter = True
    encryption = False

    def __init__(self):
        base.DataHandler.__init__(self)

    def export_data(self, entrystore, password=None):
        """Exports data to a CSV file"""

        # fetch and sort entries
        entries = []
        iter = entrystore.iter_nth_child(None, 0)

        while iter is not None:
            e = entrystore.get_entry(iter)

            if type(e) != entry.FolderEntry:
                entries.append(e)

            iter = entrystore.iter_traverse_next(iter)

        entries.sort(lambda x, y: cmp(x.name.lower(), y.name.lower()))

        stringwriter = StringIO()
        csvwriter = csv.writer(stringwriter, dialect="excel")

        keys = set()
        for e in entries:
            for f in e.fields:
                keys.add(f.name)

        # 'Email', 'Hostname', 'Password', 'URL', 'Username'
        keys = sorted(keys)

        csvwriter.writerow(['Name', 'Type', 'Description', 'Updated'] + keys)

        for e in entries:

            values = []
            for key in keys:
                value = ''
                for field in e.fields:
                    if key == field.name:
                        value = field.value
                values.append(value)

            updated = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.updated))
            csvwriter.writerow([e.name, e.typename, e.description, updated] + values)

        return stringwriter.getvalue()
