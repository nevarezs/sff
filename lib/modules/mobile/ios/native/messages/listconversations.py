"""Smartphone Framework Forensics
    Module: mobile/ios/native/messages/list.
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
# Regular expression operations
# https://docs.python.org/2/library/re.html
import re

# Helper methods that interact with the iOS contacts database
from lib.common.mobile.ios import contacts_helper
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

    mobile/ios/native/messages/list
        This module uses the SMS/iMessage db and optionally
        the contacts db (i.e., the Address Book) in the iOS Backup
        to output a list of conversations related to the Messages
        app that are stored on the device (i.e., using the iOS Backup).
    """
    info = {
        "name": "List iOS conversations",
        "author": "Sergio Nevarez",
        "description": "Lists conversations from " \
            + "native iOS Messages application",
        "options": [
            [
             "OUTPUT_FILE_NAME_PREFIX", # Option Name
             "conversationlist", # Value
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
             "SERVICE", # Option Name
             "any", # Value
             True, # Required Option
             "Show only conversations from a " \
                + "specific service. " \
                + "Valid options are: any,imessage,sms" # Description
            ],
            [
             "SHOW_CONTACT_INFO", # Option Name
             False, # Value
             True, # Required Option
             "Find contact information in Address Book" # Description
            ]
        ]
    }

    def __init__(self):
        """Initializes module.

        Sets require_sms property to True so that IOSModule
        validates that the SMS/iMessage db is present in the backup directory.

        Sets require_contacts property to True so that IOSModule
        validates that the contacts db is present in the backup directory.
        """
        IOSModule.__init__(self,
            "lib/modules/mobile/ios/native/messages/listconversations.conf")
        self.require_contacts = True
        self.require_sms = True

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def run(self):
        """Run module's code."""
        conversations = self._get_conversation_list()

        # Output
        title = "Conversation List"
        header = None
        output_format = self.get_option_value("OUTPUT_FORMAT").lower()
        if (output_format == "stdout"):
            print title
            self._print_table(conversations)
        elif (output_format == "html"):
            if (not os.path.isdir(self.output_dir)):
                os.mkdir(self.output_dir)
            output_prefix = self.get_option_value("OUTPUT_FILE_NAME_PREFIX")
            file_full_path = self.output_dir + "/" + output_prefix + ".html"
            html.create_document_from_row_list(title,
                header,
                conversations,
                file_full_path)
            print "Output saved to: " + file_full_path
        elif (output_format == "pdf"):
            if (not os.path.isdir(self.output_dir)):
                os.mkdir(self.output_dir)
            output_prefix = self.get_option_value("OUTPUT_FILE_NAME_PREFIX")
            file_full_path = self.output_dir + "/" + output_prefix + ".pdf"
            pdf.create_document_from_row_list(title,
                header,
                conversations,
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
        headers.append("ID")
        headers.append("Phone Number / Email Address")
        if (self.get_option_value("SHOW_CONTACT_INFO")):
            headers.append("Name")
        headers.append("Service")
        return headers

    def _get_conversation_list(self):
        """Query the SMS/iMessage DB to get the list of conversations.

        If the SHOW_CONTACT_INFO option is set to true,
        attempt to find contact information (i.e., Name) from
        each person that is part of a conversation.

        Returns
          List of tuples with information from the SMS/iMessage DB."
        """
        query = self._get_query()
        service = self.get_option_value("SERVICE")
        if (service == "any"):
            rows = db.query(self.sms_db_path, query)
        else:
            params = [service]
            rows = db.query(self.sms_db_path, query, tuple(params))

        if (self.get_option_value("SHOW_CONTACT_INFO")):
            # SHOW_CONTACT_INFO = True
            rows_with_contact_info = [self._get_headers()]
            for r in rows:
                # The 'id' in the following function name
                # refers to the "handle id" which is the
                # phone number or email address that
                # is stored in the handle table within the
                # messages db.
                name = \
                    contacts_helper.get_contact_by_id(self.backup_dir, r[1])
                rows_with_contact_info.append((r[0], r[1], name, r[2]))
            return rows_with_contact_info

        # SHOW_CONTACT_INFO = False
        rows.insert(0, self._get_headers())
        return rows

    def _get_query(self):
        """Create SQL statement to query the messages DB.

        The statement is created based on the value set
        to each of the options supported by this module.
        """
        service = self.get_option_value("SERVICE")
        q_select = "SELECT c.rowid, h.id, h.service"
        q_from = "FROM chat c, handle h"
        q_join = "JOIN chat_handle_join chj " \
                    + "ON chj.handle_id = h.rowid " \
                    + "and chj.chat_id = c.rowid"
        q_where = "WHERE h.service = ?"
        q_case_insensitive = "COLLATE NOCASE"
        if (service == "any"):
            query = " ".join([q_select, q_from, q_join, q_case_insensitive])
        else:
            query = " ".join(
                [q_select, q_from, q_join, q_where, q_case_insensitive])
        return query
