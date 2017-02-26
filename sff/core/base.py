"""Smartphone Framework Forensics
    Class for the program's command line menu/interpreter.
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

# The framework module contains the ForensicsFramework class.
from sff.core import framework

class Forensics(framework.ForensicsFramework):
    """Class for the program's command line menu/interpreter.

    This class implement the functionality supported by the
    application's main command line menu/interpreter.
    """
    def __init__(self):
        """Initializes Forensics class
        by setting the list of supported modules.

        Args:
          self: Reference to the instance of the class.
        """
        framework.ForensicsFramework.__init__(self)
        # Supported modules
        self._modules = [
            ["Module ID", "Module Name", "Description"],
            ["1", "mobile/ios/native/contacts/list",
                "Lists contacts from native iOS Address Book"],
            ["2", "mobile/ios/native/messages/extract_conversations",
                "Extract conversation contents from iOS Messages DB"],
            ["3", "mobile/ios/native/messages/list",
                "Lists conversations from native iOS Messages DB"]
        ]

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def do_show(self, line):
        """Implementation of the 'show' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'show' command.
        """
        if not line:
            # The 'show' command expects an option as its argument.
            # Display command documentation.
            self.help_show()
            return

        # Options are case-insensitive
        option = line.lower()
        if (option == "modules"):
            # Display the list of supported modules.
            self._show_modules()
        else:
            # Unsupported option.
            # Display command documentation for a list of valid options.
            print "Option \"" + option + "\" not supported\n"
            self._show_supported_options()

    def do_use(self, line):
        """Implementation of the 'use' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'use' command.
        """
        if not line:
            # The 'use' command expects a module as its argument.
            # Display command documentation.
            self.help_use()
            return

        if line == "mobile/ios/native/contacts/list" \
            or line == "1":
            # Load and start mobile/ios/native/contacts/list module.
            from lib.modules.mobile.ios.native.contacts.listcontacts \
                import Module
            mod = Module()
            mod.prompt = "(mobile/ios/native/contacts/list) > "
            mod.cmdloop()
            return
        if line == "mobile/ios/native/messages/extract_conversations" \
            or line == "2":
            # Load and start mobile/ios/native/messages/list module.
            from lib.modules.mobile.ios.native.messages.extractconversations \
                import Module
            mod = Module()
            mod.prompt = "(mobile/ios/native/messages/extract_conversations) > "
            mod.cmdloop()
            return
        if line == "mobile/ios/native/messages/list" \
            or line == "3":
            # Load and start mobile/ios/native/messages/list module.
            from lib.modules.mobile.ios.native.messages.listconversations \
                import Module
            mod = Module()
            mod.prompt = "(mobile/ios/native/messages/list) > "
            mod.cmdloop()
            return

        # Unusupported module.
        print "Module '%s' not implemented" % line

    # ***************************************************************
    # HELP
    # ***************************************************************

    def help_show(self):
        """Print the 'show' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\tshow -- Show information.",
                         "SYNOPSYS",
                         "\tshow <option>",
                         "DESCRIPTION",
                         "\tShow information based on the option selected."
                         ])
        self._show_supported_options()

    def help_use(self):
        """Print the 'use' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\tuse -- Load module.",
                         "SYNOPSYS",
                         "\tuse <[module name | module id]>",
                         "DESCRIPTION",
                         "\tLoad and interact with module."
                         ])

    # ***************************************************************
    # HELPER methods
    # ***************************************************************

    def _show_modules(self):
        """Display the list of supported modules."""
        self._print_table(self._modules)

    def _show_supported_options(self):
        """Show list of supported options for the 'show' command.

        Args:
          self: Reference to the instance of the class.
        """
        options = [
            ["Option", "Description"],
            ["modules", "Show list of supported modules"]
        ]
        print "SUPPORTED OPTIONS"
        self._print_table(options)