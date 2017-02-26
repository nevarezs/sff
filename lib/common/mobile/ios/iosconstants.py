"""Smartphone Framework Forensics
    Defines a set of constants related to iOS backup resources.
    Copyright (C) 2017  Sergio A. Nevarez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class Backup(object):
    """The Backup class defines a set of constants related to iOS backups."""
    CONTACT_IMAGES_DB_FILE_NAME = \
        "HomeDomain-Library/AddressBook/AddressBookImages.sqlitedb"
    CONTACT_IMAGES_DB_FILE_NAME_HASH = \
        "cd6702cea29fe89cf280a76794405adb17f9a0ee"

    CONTACTS_DB_FILE_NAME = \
        "HomeDomain-Library/AddressBook/AddressBook.sqlitedb"
    CONTACTS_DB_FILE_NAME_HASH = \
        "31bb7ba8914766d4ba40d6dfb6113c8b614be442"

    MESSAGES_DB_FILE_NAME = \
        "HomeDomain-Library/SMS/sms.db"
    MESSSAGES_DB_FILE_NAME_HASH = \
        "3d0d7e5fb2ce288813306e4d4636395e047a3d28"
