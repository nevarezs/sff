"""Smartphone Framework Forensics
    Functions to export output to HTML.
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

# System-specific parameters and functions
# https://docs.python.org/2/library/sys.html
import sys

try:
    # Python library for generating HTML
    # http://www.yattag.org/
    from yattag import Doc
    from yattag import indent
except ImportError as e:
    # At least one of the required modules is not installed
    # on this system.
    print "Module \"{0}\" not installed".format(e.message[16:])
    # Exit program
    sys.exit(1)

def create_document_from_row_list(title, header, row_list,
    file_path):
    """Create and save HTML5 document from a table.

    Args:
      title: The title that will be used on the document.
      row_list: List of rows containing the data
      file_path: full path of the pdf document to save
    """
    with open(file_path, "w+") as output_file:
        output_file.write(
            generate_document_from_row_list(
                title, header, row_list).encode('ascii', 'xmlcharrefreplace')
        )

def generate_document_from_row_list(title, header, row_list):
    """Create HTML5 document from a table.

    Args:
      title: Title of html document.
      row_list: Table with the data to generate the document.
    """
    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.asis("<meta charset=\"utf-8\">")
            with tag("title"):
                text(title)
        with tag("body"):
            with tag("h1"):
                text(title)
            if (header is not None):
                with tag("h3"):
                    text(header)
            with tag("table", border="1"):
                for r in row_list:
                    num_cols = len(r)
                    with tag("tr"):
                        for i in range(num_cols):
                            with tag("td"):
                                if r[i] is None:
                                    text("")
                                elif unicode(r[i]).encode(
                                    "unicode-escape").startswith("<img"):
                                    doc.asis(r[i])
                                else:
                                    text(r[i])
    return doc.getvalue()
