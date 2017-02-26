"""Smartphone Framework Forensics
    Base class used to implement the application's
    command line menu/interpreter.
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

# Support for line-oriented command interpreters
# https://pymotw.com/2/cmd/
# https://docs.python.org/2/library/cmd.html
import cmd
# Basic date and time types
# https://docs.python.org/2/library/datetime.html
from datetime import datetime
# System-specific parameters and functions
# https://docs.python.org/2/library/sys.html
import sys
# Text wrapping and filling
# https://docs.python.org/2/library/textwrap.html
from textwrap import wrap

try:
    # https://pypi.python.org/pypi/terminaltables
    from terminaltables import AsciiTable
except ImportError as e:
    # At least one of the required modules is not installed
    # on this system.
    print "Module \"{0}\" not installed".format(e.message[16:])
    # Exit program
    sys.exit(1)

class ForensicsFramework(cmd.Cmd):
    """Base class for the command line menus/interpreters.

    This class implements common functionality that is used by
    the application's main menu and by menus implemented by modules.

    This class inherits from Python's Cmd class
      (see https://docs.python.org/2/library/cmd.html)
    """
    def __init__(self):
        """Initializes ForensicsFramework class
        by setting the banner to display.
        """
        cmd.Cmd.__init__(self)
        # Set the banner to display when the application starts
        self.intro = "Smartphone Framework Forensics " \
            + "Copyright (C) 2017 Sergio A. Nevarez\n" \
            + "This program comes with ABSOLUTELY NO WARRANTY.\n" \
            + "This is free software, and you are welcome to redistribute " \
            + "it under certain conditions.\n" \
            + "See LICENSE file for details or see " \
            + "GNU GPL Version 3 <http://www.gnu.org/licenses/>.\n" \
            + "\n" \
            + "Type 'help' for list of available commands."
        # ASCII art created using the following link
        # http://patorjk.com/software/taag/#p=display&f=Big&t=forensics
        self.intro += """
   __
  / _|                       (_)
 | |_ ___  _ __ ___ _ __  ___ _  ___ ___
 |  _/ _ \| '__/ _ \ '_ \/ __| |/ __/ __|
 | || (_) | | |  __/ | | \__ \ | (__\__ \\
 |_| \___/|_|  \___|_| |_|___/_|\___|___/
        """

        # Set the prompt for the command line interpreter
        self.prompt = "(SFF) > "

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def do_exit(self, line):
        """Implementation of the 'exit' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'exit' command (unused).
        """
        sys.exit(0)

    # ***************************************************************
    # HELP
    # ***************************************************************

    def help_exit(self):
        """Print the 'exit' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\texit -- Terminate application",
                         "SYNOPSYS",
                         "\texit",
                         "DESCRIPTION",
                         "\tExits command line interpreter."
                         ])

    # ***************************************************************
    # OUTPUT
    # ***************************************************************

    def _print_table(self, data):
        """Print table to stdout."""
        max_width = 45
        wrapped_data = \
            [["\n".join(wrap(col, max_width))
                if ((type(col) is str or type(col) is unicode)
                    and len(col) > max_width)
                else col
                for col in row]
                for row in data]
        table = AsciiTable(wrapped_data)
        table.inner_row_border = True
        print table.table