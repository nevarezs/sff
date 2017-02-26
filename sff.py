#!/usr/bin/env python

"""Smartphone Framework Forensics
    This is the entry point to the application.
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

__author__ = "Sergio Nevarez"

# Import Forensics class, which implements the main menu
from sff.core.base import Forensics

# ************************* MAIN *********************************************
def main():
    """Start the application loop to read user input."""
    Forensics().cmdloop()

if __name__ == "__main__":
    # Code to run if this is called from the command line.
    main()