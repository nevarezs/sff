"""Smartphone Framework Forensics
    Module: mobile/ios/native/contacts/list.
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

# Miscellaneous operating system interfaces
# https://docs.python.org/2/library/os.html
import os

# The db module includes the code to run queries on sqlite databases.
from lib.common.db.sqlite import db
# The ioscontants module contains the names of important iOS backup files.
from lib.common.mobile.ios import iosconstants
# The html module contains functions to generate html output
from lib.export import html
# The pdf module contains functions to generate pdf output
from lib.export import pdf
# IOS module is the Base class for modules that need an iOS Backups.
from sff.core.module import IOSModule

class Module(IOSModule):
    """The Module class implements the current module's code.

    mobile/ios/native/contacts/list
        This module uses the contacts db (i.e., the Address Book)
        in the iOS Backup to output a list of contacts that were
        stored on the device.
    """
    info = {
        "name": "List iOS contacts",
        "author": "Sergio Nevarez",
        "description": "Lists contacts from native iOS Address Book",
        "options": [
            [
             "INCLUDE_ID", # Option Name
             True, # Value
             True, # Required Option
             "Include contact DB ID in the output." # Description
            ],
            [
             "INCLUDE_ORGANIZATION", # Option Name
             True, # Value
             True, # Required Option
             "Include 'Organization' name in the output." # Description
            ],
            [
             "KEYWORDS", # Option Name
             "", # Value
             False, # Required Option
             "Comma-separated list of keywords to filter the output. " \
             + "The keywords are used to search by name, organization, or " \
             + "value (e.g., phone number or e-mail address.)"
            ],
            [
             "OUTPUT_FILE_NAME_PREFIX", # Option Name
             "contacts", # Value
             True, # Required Option
             "Output file name prefix for pdf and html files."
            ],
            [
             "OUTPUT_FORMAT", # Option Name
             "stdout", # Value
             True, # Required Option
             "Valid options: stdout,pdf,html"
            ],
            [
             "SPLIT_NAME", # Option Name
             False, # Value
             True, # Required Option
             "Show First and Last names as separate columns." # Description
            ]
        ]
    }

    def __init__(self):
        """Initializes module.

        Sets require_contacts property to True so that IOSModule
        validates that the contacts db is present in the backup directory.
        """
        IOSModule.__init__(self,
            "lib/modules/mobile/ios/native/contacts/listcontacts.conf")
        self.require_contacts = True

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def run(self):
        """Run module's code."""
        contacts = self._list_contacts()

        # Output
        title = "Contacts"
        header = None
        output_format = self.get_option_value("OUTPUT_FORMAT").lower()
        if (output_format == "stdout"):
            print title
            self._print_table(contacts)
        elif (output_format == "html"):
            if (not os.path.isdir(self.output_dir)):
                os.mkdir(self.output_dir)
            output_prefix = self.get_option_value("OUTPUT_FILE_NAME_PREFIX")
            file_full_path = self.output_dir + "/" + output_prefix + ".html"
            html.create_document_from_row_list(title,
                header,
                contacts,
                file_full_path)
            print "Output saved to: " + file_full_path
        elif (output_format == "pdf"):
            if (not os.path.isdir(self.output_dir)):
                os.mkdir(self.output_dir)
            output_prefix = self.get_option_value("OUTPUT_FILE_NAME_PREFIX")
            file_full_path = self.output_dir + "/" + output_prefix + ".pdf"
            pdf.create_document_from_row_list(title,
                header,
                contacts,
                file_full_path)
            print "Output saved to: " + file_full_path
        else:
            print "Unsupported OUTPUT_FORMAT"

    # ***************************************************************
    # HELPER methods
    # ***************************************************************

    def _get_headers(self):
        """Get headers for output table.

        The list of headers is based on the value set
        to each of the options supported by this module.
        """
        headers = []
        if (self.get_option_value("INCLUDE_ID")):
            headers.append("ID")
        if (self.get_option_value("SPLIT_NAME")):
            headers.append("First Name")
            headers.append("Last Name")
        else:
            headers.append("Name")
        if (self.get_option_value("INCLUDE_ORGANIZATION")):
            headers.append("Organization")
        headers.append("Type")
        headers.append("Value")
        return headers

    def _get_query(self):
        """Create SQL statement to query the contacts DB.

        The statement is created based on the value set
        to each of the options supported by this module.
        """
        q_select = "SELECT "
        if (self.get_option_value("INCLUDE_ID")):
            q_select += "p.rowid, "
        if (self.get_option_value("SPLIT_NAME")):
            q_select += "p.first, p.last, "
        else:
            q_select += "coalesce(p.first, '') || ' ' || " \
                        + "coalesce(p.last, '') as Name, "
        if (self.get_option_value("INCLUDE_ORGANIZATION")):
            q_select += "p.organization, "
        q_select += "case " \
                    + "when m.label in " \
                        + "(select rowid from abmultivaluelabel) " \
                    + "then (select value " \
                        + "from abmultivaluelabel " \
                        + "where m.label = rowid) " \
                    + "else m.label " \
                    + "end as Type, " \
                    + "m.value"
        q_from = "from " \
                    + "abperson p, " \
                    + "abmultivalue m"
        q_where = "where " \
                    + "p.rowid=m.record_id " \
                    + "and m.value not null"
        keywords = \
            [k.strip()
                for k in str(self.get_option_value("KEYWORDS")).split(",")]
        i = 0
        for k in keywords:
            if (self.get_option_value("SPLIT_NAME")):
                if (i == 0):
                    q_where += " and ((m.value like ? " \
                        + "or p.first like ? or p.last like ?)"
                else:
                    q_where += " or (m.value like ? " \
                        + "or p.first like ? or p.last like ?)"
            else:
                if (i == 0):
                    q_where += " and ((m.value like ? or Name like ?)"
                else:
                    q_where += " or (m.value like ? or Name like ?)"
            i += 1
        if (len(keywords) > 0):
            q_where += ")"
        q_order_by = "order by " \
                    + "p.rowid"
        query = " ".join([q_select, q_from, q_where, q_order_by])
        return query

    def _list_contacts(self):
        """Query the Address Book to get contact information.

        Returns
          List of tuples with information from the Address Book."
        """
        query = self._get_query()
        keywords = \
            [k.strip()
                for k in str(self.get_option_value("KEYWORDS")).split(",")]
        params = []
        for k in keywords:
            p = '%' + str(k) + '%'
            if (self.get_option_value("SPLIT_NAME")):
                params.extend([p, p, p])
            else:
                params.extend([p, p])
        rows = db.query(self.contacts_db_path,
                        query, tuple(params))
        rows.insert(0,
            self._get_headers())
        return rows
