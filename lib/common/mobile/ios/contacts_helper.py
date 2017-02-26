"""Smartphone Framework Forensics
    Helper functions to interact with the contacts db.
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

# Regular expression operations
# https://docs.python.org/2/library/re.html
import re

# DB-API 2.0 interface for SQLite databases
# https://docs.python.org/2/library/sqlite3.html
import sqlite3

# The db module includes the code to run queries on sqlite databases.
from lib.common.db.sqlite import db

try:
    # https://pypi.python.org/pypi/phonenumberslite
    import phonenumbers
except ImportError as e:
    # At least one of the required modules is not installed
    # on this system.
    print "Module \"{0}\" not installed".format(e.message[16:])
    # Exit program
    sys.exit(1)

CONTACTS_DATABASE_FILE_NAME = \
    "HomeDomain-Library/AddressBook/AddressBook.sqlitedb"
CONTACTS_DATABASE_FILE_NAME_HASH = \
    "31bb7ba8914766d4ba40d6dfb6113c8b614be442"

def get_contact_by_id(backup_dir, id):
    if ("@" in id):
        # Treat as email address
        contact_id = id
        rows = list_contacts(backup_dir)
        for r in rows:
            contact_value = r[2]
            if ("@" in contact_value):
                if contact_id in contact_value:
                    if (r[1] is not None):
                        return str(r[1])
    else:
        return get_contact_by_phone_number(backup_dir, id)

    return ""

def get_contact_by_phone_number(backup_dir, full_number):
    try:
        number = phonenumbers.parse(full_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return ""

    number_no_country_code = str(number.national_number)
    rows = list_contacts(backup_dir)
    for r in rows:
        contact_value = r[2]
        contact_number = re.sub(r"[^0-9]", "", contact_value)
        if number_no_country_code in contact_number:
            if (r[1] is not None):
                return str(r[1])

    return ""

def list_contacts(backup_dir):
    path = backup_dir + "/" + CONTACTS_DATABASE_FILE_NAME_HASH
    query = "SELECT " \
                + "p.rowid, " \
                + "coalesce(p.first, '') || ' ' || " \
                + "coalesce(p.last, '') as Name, " \
                + "m.value " \
            + "from " \
                + "abperson p, " \
                + "abmultivalue m " \
            + "where " \
                + "p.rowid=m.record_id and m.value not null " \
            + "order by " \
                + "p.rowid"
    rows = db.query(path,
                    query)
    rows.insert(0, ('ID', 'Name', 'Value'))
    return rows