"""Smartphone Framework Forensics
    Module: mobile/ios/native/messages/extract_conversations.
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

# Convert between binary and ASCII
# https://docs.python.org/2/library/binascii.html
import binascii
# Secure hashes and message digests
# https://docs.python.org/2/library/hashlib.html
import hashlib
# Functions creating iterators for efficient looping
# https://docs.python.org/2/library/itertools.html
import itertools
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

    mobile/ios/native/messages/extract_conversations
        This module uses the SMS/iMessage db and optionally
        the contacts db (i.e., the Address Book) in the iOS Backup
        to extract the content of conversations related to the Messages
        app that are stored on the device (i.e., using the iOS Backup).
    """
    info = {
        "name": "Extract Conversations",
        "author": "Sergio Nevarez",
        "description": "Extract conversations from " \
            + "native iOS Messages application",
        "options": [
            [
             "CONVERSATION_IDS", # Option Name
             "", # Value
             True, # Required Option
             "Comma-separated list with IDs of " \
             + "the conversations to extract. " \
             + "Use the 'messages/list' module to get " \
             + "a list of conversations stored on the device."
            ],
            [
             "END_DATE", # Option Name
             "", # Value
             False, # Required Option
             "Only include messages on or before this date. " \
                + "Format: YYYY-MM-DD." # Description
            ],
            [
             "INCLUDE_MESSAGE_ID", # Option Name
             True, # Value
             True, # Required Option
             "Include message ID for " \
                + "each message in the output." # Description
            ],
            [
             "INCLUDE_SERVICE", # Option Name
             True, # Value
             True, # Required Option
             "Include Service (i.e., 'SMS'/'iMessage') " \
                + "in the output." # Description
            ],
            [
             "INCLUDE_SUBJECT", # Option Name
             False, # Value
             True, # Required Option
             "Include conversation 'Subject' in the output." # Description
            ],
            [
             "KEYWORDS", # Option Name
             "", # Value
             False, # Required Option
             "Comma-separated list of keywords to filter the output. " \
             + "The keywords are used to search in the content of the " \
             + "messages."
            ],
            [
             "OUTPUT_FILE_NAME_PREFIX", # Option Name
             "conversation", # Value
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
             "SHOW_CONTACT_INFO", # Option Name
             False, # Value
             True, # Required Option
             "Find contact information in Address Book" # Description
            ],
            [
             "START_DATE", # Option Name
             "", # Value
             False, # Required Option
             "Only include messages on or after this date. " \
                + "Format: YYYY-MM-DD." # Description
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
            "lib/modules/mobile/ios/native/messages/" \
            + "extractconversations.conf")
        self.require_contacts = True
        self.require_sms = True

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def run(self):
        """Run module's code."""
        conversations = self._get_conversations()

        # Output
        output_format = self.get_option_value("OUTPUT_FORMAT").lower()
        if (output_format != "stdout"
            and output_format != "html"
            and output_format != "pdf"):
            print "Unsupported OUTPUT_FORMAT"
            return

        for c in conversations:
            conversation_id = str(c[0])
            people = c[1]
            conversation = [list(t) for t in c[2]]
            title = "Conversation ID: " + conversation_id
            header = ""
            if (self.get_option_value("SHOW_CONTACT_INFO")):
                header = "People involved in the conversation " \
                    + "(from Address Book): " \
                    + ", ".join(people)
            if (output_format == "stdout"):
                print title
                print header
                # Remove attachment (i.e., image) references from the data
                # because they will not display properly in
                # stdout.
                num_cols = len(conversation[0])
                for r in conversation:
                    text = r[num_cols - 1]
                    # Convert to hex to search for the
                    # object replacement character
                    text = binascii.hexlify(text.encode("utf-8"))
                    # 0xEF 0xBF 0xBC is the object replacement character
                    # For reference:
                    # http://www.fileformat.info/info/unicode/char/fffc/index.htm
                    result = re.split(r"efbfbc", text)
                    is_image_at_the_end = False
                    if (len(result) == 2):
                        attachment_reference = binascii.unhexlify(result[0])
                        if (len(attachment_reference) > 0):
                            ref = re.split(r";", attachment_reference, 2)
                            if (len(ref[2]) > 0):
                                is_image_at_the_end = True
                                text = str(ref[2])
                        # Remove reference to attachment
                        # and keep object replacement character
                        result[0] = binascii.unhexlify(
                            "efbfbc").decode("utf-8")
                        if (len(result[1]) > 0):
                            result[1] = binascii.unhexlify(
                                result[1]).decode("utf-8")
                        elif (is_image_at_the_end):
                            result[1] = text
                    else:
                        result[0] = binascii.unhexlify(
                            result[0]).decode("utf-8")
                    if (is_image_at_the_end):
                        r[num_cols - 1] = "".join(reversed(result))
                    else:
                        r[num_cols - 1] = "".join(result)
                self._print_table(conversation)
            elif (output_format == "html"):
                if (not os.path.isdir(self.output_dir)):
                    os.mkdir(self.output_dir)
                output_prefix = \
                    self.get_option_value("OUTPUT_FILE_NAME_PREFIX") \
                    + conversation_id
                file_full_path = \
                    self.output_dir + "/" + output_prefix + ".html"
                num_cols = len(conversation[0])
                for r in conversation:
                    text = r[num_cols - 1]
                    # Convert to hex to search for the
                    # object replacement character
                    text = binascii.hexlify(text.encode("utf-8"))
                    # 0xEF 0xBF 0xBC is the object replacement character
                    # For reference:
                    # http://www.fileformat.info/info/unicode/char/fffc/index.htm
                    result = re.split(r"efbfbc", text)
                    is_image_at_the_end = False
                    if (len(result) == 2):
                        # Result contains the text before
                        # and after the object replacement character
                        attachment_reference = binascii.unhexlify(result[0])
                        if (len(attachment_reference) > 0):
                            # There is a file reference to the image
                            ref = re.split(r";", attachment_reference, 2)
                            mime_type = ref[0]
                            path = ref[1]
                            if (len(ref[2]) > 0):
                                is_image_at_the_end = True
                                text = str(ref[2])
                            attachment_path = "MediaDomain-" + path[2:]
                            attachment_path = hashlib.sha1(
                                attachment_path).hexdigest()
                            attachment_path = \
                                self.backup_dir + "/" + attachment_path
                            # check if file exists
                            if (os.path.isfile(attachment_path)):
                                with open(attachment_path, "r") as attachment:
                                    img = '<img style=' \
                                        + '"max-width: 400px; ' \
                                        + 'max-height: 400px;" src="data:' \
                                        + mime_type + ';base64,' \
                                        + binascii.b2a_base64(
                                            attachment.read()) \
                                        + '" /><br>'
                        result[0] = img
                        if (len(result[1]) > 0):
                            result[1] = binascii.unhexlify(
                                result[1]).decode("utf-8")
                        elif (is_image_at_the_end):
                            result[1] = text
                    else:
                        result[0] = binascii.unhexlify(
                            result[0]).decode("utf-8")
                    r[num_cols - 1] = "".join(result)
                html.create_document_from_row_list(title,
                    header,
                    conversation,
                    file_full_path)
                print "Output saved to: " + file_full_path
            elif (output_format == "pdf"):
                if (not os.path.isdir(self.output_dir)):
                    os.mkdir(self.output_dir)
                output_prefix = \
                    self.get_option_value("OUTPUT_FILE_NAME_PREFIX") \
                    + conversation_id
                file_full_path = \
                    self.output_dir + "/" + output_prefix + ".pdf"
                num_cols = len(conversation[0])
                for r in conversation:
                    text = r[num_cols - 1]
                    # Convert to hex to search for the
                    # object replacement character
                    text = binascii.hexlify(text.encode("utf-8"))
                    # 0xEF 0xBF 0xBC is the object replacement character
                    # For reference:
                    # http://www.fileformat.info/info/unicode/char/fffc/index.htm
                    result = re.split(r"efbfbc", text)
                    is_image_at_the_end = False
                    if (len(result) == 2):
                        # Result contains the text before
                        # and after the object replacement character
                        attachment_reference = binascii.unhexlify(result[0])
                        if (len(attachment_reference) > 0):
                            # There is a file reference to the image
                            ref = re.split(r";", attachment_reference, 2)
                            mime_type = ref[0]
                            path = ref[1]
                            if (len(ref[2]) > 0):
                                is_image_at_the_end = True
                                text = str(ref[2])
                            attachment_path = "MediaDomain-" + path[2:]
                            attachment_path = hashlib.sha1(
                                attachment_path).hexdigest()
                            attachment_path = \
                                self.backup_dir + "/" + attachment_path
                            # check if file exists
                            if (os.path.isfile(attachment_path)):
                                with open(attachment_path, "r") as attachment:
                                    img = '<img style=' \
                                        + '"max-width: 400px; ' \
                                        + 'max-height: 400px;" src="data:' \
                                        + mime_type + ';base64,' \
                                        + binascii.b2a_base64(
                                            attachment.read()) \
                                        + '" /><br>'
                        result[0] = img
                        if (len(result[1]) > 0):
                            result[1] = binascii.unhexlify(
                                result[1]).decode("utf-8")
                        elif (is_image_at_the_end):
                            result[1] = text
                    else:
                        result[0] = binascii.unhexlify(
                            result[0]).decode("utf-8")
                    r[num_cols - 1] = "".join(result)
                pdf.create_document_from_row_list(title,
                    header,
                    conversation,
                    file_full_path,
                    True)
                print "Output saved to: " + file_full_path

    # ***************************************************************
    # HELPER methods
    # ***************************************************************

    def _get_headers(self):
        """Get headers for output table.

        The list of headers is based on the value set
        to each of the options supported by this module.
        """
        headers = []
        if (self.get_option_value("INCLUDE_MESSAGE_ID")):
            headers.append("ID")
        headers.append("Date")
        headers.append("Phone / Email")
        if (self.get_option_value("INCLUDE_SERVICE")):
            headers.append("Service")
        headers.append("Sent/Received")
        if (self.get_option_value("INCLUDE_SUBJECT")):
            headers.append("Subject")
        headers.append("Text")
        return headers

    def _get_conversations(self):
        """Query the SMS/iMessage DB to get the list of conversations.

        If the SHOW_CONTACT_INFO option is set to true,
        attempt to find contact information (i.e., Name) from
        each person that is part of the conversation.

        Returns
          List of tuples with information from the SMS/iMessage DB."
        """
        query = self._get_query()
        ids = \
            [id.strip()
                for id in str(self.get_option_value(
                    "CONVERSATION_IDS")).split(",")]
        conversations = []
        ids = list(itertools.chain.from_iterable(
            [range(int(r[0]), int(r[1]) + 1)
                if len(r) == 2
                else [int(r[0])]
                for r in
                    [id.split("-") for id in ids]])
        )
        for id in ids:
            params = [id]
            keywords = \
                [k.strip()
                    for k in str(
                        self.get_option_value("KEYWORDS")).split(",")]
            for k in keywords:
                params.append('%' + str(k) + '%')
            # Only include messages between
            # START_DATE and END_DATE (inclusive)
            # if those options are set.
            start_date = self.get_option_value("START_DATE")
            end_date = self.get_option_value("END_DATE")
            if (start_date != ""):
                params.append(start_date)
            if (end_date != ""):
                params.append(end_date)
            people = []
            if (self.get_option_value("SHOW_CONTACT_INFO")):
                query_phone_numbers = "SELECT h.id " \
                + "FROM chat c, handle h " \
                + "JOIN chat_handle_join chj " \
                + "ON chj.handle_id = h.rowid " \
                    + "and chj.chat_id = c.rowid " \
                + "WHERE c.rowid = " + str(id) + " " \
                + "COLLATE NOCASE"
                phone_numbers = db.query(
                    self.sms_db_path, query_phone_numbers)
                for p in phone_numbers:
                    name = \
                        contacts_helper.get_contact_by_id(
                            self.backup_dir, p[0])
                    people.append((name, p[0]))
                people = [p[0] + " (" + p[1] + ")" for p in people]
            conversation = db.query(self.sms_db_path,
                            query, tuple(params))
            if (len(conversation) > 0):
                conversation.insert(0,
                    self._get_headers())
                conversations.append((id, people, conversation))
        return conversations

    def _get_query(self):
        """Create SQL statement to query the messages DB.

        The statement is created based on the value set
        to each of the options supported by this module.
        """
        q_select = "SELECT "
        if (self.get_option_value("INCLUDE_MESSAGE_ID")):
            q_select += "m.rowid as MsgID, "
        # Using the DATETIME sqlite function to convert the time
        # from Mac Absolute Time to Unix epoch time and then
        # to localtime.
        # For reference:
        # https://linuxsleuthing.blogspot.com/2012/10/whos-texting-ios6-smsdb.html
        q_select += "DATETIME(m.date + 978307200, 'unixepoch', 'localtime')" \
                    + " as d, "
        q_select += "h.id as 'Phone Number / Email Address', "
        if (self.get_option_value("INCLUDE_SERVICE")):
            q_select += "m.service as Service, "
        q_select += "CASE is_from_me "
        q_select += "WHEN 0 THEN 'Received' "
        q_select += "WHEN 1 THEN 'Sent' "
        q_select += "ELSE 'Unknown' "
        q_select += "END as Type, "
        if (self.get_option_value("INCLUDE_SUBJECT")):
            q_select += "CASE "
            q_select += "WHEN m.subject IS NULL THEN '' "
            q_select += "ELSE m.subject "
            q_select += "END as Subject, "
        q_select += "CASE "
        q_select += "WHEN m.text IS NULL THEN '' "
        q_select += "WHEN hex(m.text) like '%EFBFBC%' THEN "
        q_select += "CASE WHEN ("
        q_select += "SELECT COUNT(*) from attachment a, message msg "
        q_select += "JOIN message_attachment_join maj "
        q_select += "ON maj.attachment_id = a.rowid "
        q_select += "and maj.message_id = msg.rowid "
        q_select += "WHERE a.mime_type like 'image/%' "
        q_select += "and msg.rowid = m.rowid"
        q_select += ") > 0 THEN "
        q_select += "coalesce("
        q_select += "(SELECT a.mime_type from attachment a, message msg "
        q_select += "JOIN message_attachment_join maj "
        q_select += "on maj.attachment_id = a.rowid "
        q_select += "and maj.message_id = msg.rowid "
        q_select += "WHERE a.mime_type like 'image/%' "
        q_select += "and msg.rowid = m.rowid), "
        q_select += "'') || ';' || "
        q_select += "coalesce("
        q_select += "(SELECT a.filename from attachment a, message msg "
        q_select += "JOIN message_attachment_join maj "
        q_select += "on maj.attachment_id = a.rowid "
        q_select += "and maj.message_id = msg.rowid "
        q_select += "WHERE a.mime_type like 'image/%' "
        q_select += "and msg.rowid = m.rowid), "
        q_select += "'') || ';' "
        q_select += "|| m.text ELSE m.text END "
        q_select += "ELSE m.text "
        q_select += "END as Text "
        q_from = "FROM "
        q_from += "message m, "
        q_from += "handle h, "
        q_from += "chat c"
        q_join = "JOIN chat_message_join cmj "
        q_join += "ON cmj.message_id = m.rowid "
        q_join += "and cmj.chat_id = c.rowid"
        q_where = "WHERE "
        q_where += "m.handle_id = h.rowid "
        q_where += "and c.rowid = ?"
        # Search for keywords if needed
        keywords = \
            [k.strip()
                for k in str(self.get_option_value("KEYWORDS")).split(",")]
        i = 0
        for k in keywords:
            if (i == 0):
                q_where += " and (m.text like ?"
            else:
                q_where += " or m.text like ?"
            i += 1
        if (len(keywords) > 0):
            q_where += ")"
        # Only include messages between
        # START_DATE and END_DATE (inclusive)
        # if those options are set.
        start_date = self.get_option_value("START_DATE")
        end_date = self.get_option_value("END_DATE")
        if (start_date != "" and end_date != ""):
            q_where += " and date(d) "
            q_where += " BETWEEN date(?)"
            q_where += " and date(?)"
        elif (start_date != "" and end_date == ""):
            q_where += " and date(d) >= date(?)"
        elif (start_date == "" and end_date != ""):
            q_where += " and date(d) <= date(?)"
        q_order_by = "ORDER BY m.date ASC"
        query = " ".join([q_select, q_from, q_join, q_where, q_order_by])
        return query
