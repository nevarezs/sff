"""Smartphone Framework Forensics
    Functions to export output to PDF.
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

# The html module contains functions to generate html output
from lib.export import html

try:
    # Wkhtmltopdf python wrapper to convert html to pdf
    # https://pypi.python.org/pypi/pdfkit
    import pdfkit
except ImportError as e:
    # At least one of the required modules is not installed
    # on this system.
    print "Module \"{0}\" not installed".format(e.message[16:])
    # Exit program
    sys.exit(1)

def create_document_from_row_list(title, header, row_list,
    file_path, is_landscape = False):
    """Create and save PDF document from a table.

    Args:
      title: The title that will be used on the first page of the document.
      row_list: List of rows containing the data
      file_path: full path of the pdf document to save
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }
    if (is_landscape):
        options["orientation"] = 'Landscape'
    pdfkit.from_string(
        html.generate_document_from_row_list(
            title, header, row_list).encode('unicode-escape'),
        file_path,
        options
    )