"""Smartphone Framework Forensics
    Implementation of the BaseModule and IOSModule classes.
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
# System-specific parameters and functions
# https://docs.python.org/2/library/sys.html
import sys

# The ioscontants module contains the names of important iOS backup files.
from lib.common.mobile.ios import iosconstants
# The framework module contains the ForensicsFramework class.
from sff.core import framework

class BaseModule(framework.ForensicsFramework):
    """Base class for the framework's modules.

    This class implements common functionality
    that can be reused by new modules.

    Attributes:
      info: A dictionary object that stores the module's metadata.
            The module's metadata includes: name, author, description,
            and supported options.
    """
    def __init__(self, config_file = None):
        """Initializes the Module.

        Removes the banner and sets a default prompt.
        """
        framework.ForensicsFramework.__init__(self)
        self.intro = ""
        self.prompt = "() > "
        self.app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.output_dir = self.app_path + "/output"
        if (config_file is not None):
            # Load module options from configuration file
            self.config_file = app_path + "/" + config_file
            self.load_config_file()

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def do_back(self, line):
        """Implementation of the 'back' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'back' command (unused).

        Returns:
          True to indicate that the module should exit.
            The interpreter goes back to the one who
            called this module.
        """
        return True

    def do_run(self, line):
        """Implementation of the 'run' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'run' command.
                Not used by the 'run' command.
        """
        # Validate required options
        options = self.info["options"]
        for o in options:
            if (o[2] and o[1] == ""):
                # Missing required option.
                # Display error message and return.
                print "Required option '%s' is not set." % o[0]
                return
        # All required options are set
        # The run() method should be implemented
        # by subclasses of BaseModule.
        self.run()

    def do_set(self, line):
        """Implementation of the 'set' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'set' command.
                The 'set' command expects two arguments.
                    1. option: The option to set
                    2. value: The value that the option will store.
        """
        if not line:
            # The 'set' command expects an option as its argument.
            # Display command documentation.
            self.help_set()
            return

        # The 'set' command expects two arguments
        args = re.split(r'\s+', line, 1)
        if len(args) != 2:
            # The number of arguments is not what
            # the 'set' command expects.
            # Display command documentation and return.
            self.help_set()
            return

        # Options are case-insensitive
        option = args[0].lower()
        # The second argument is the value
        value = args[1]
        if (not self.set_option_value(option, value)):
            # Option not found in module's metadata.
            # Display list of supported options.
            print "Option '%s' does not exist\n" % option
            self._show_options()

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
        if (option == "options"):
            # Show module options
            self._show_options()
        elif (option == "info"):
            # Display module metadata
            self._show_info()
        else:
            # Option not supported. Show list of valid options.
            print "Option \"" + option + "\" not supported\n"
            self.help_show()

    # ***************************************************************
    # HELP
    # ***************************************************************

    def help_back(self):
        """Print the 'back' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\tback -- Exit current context.",
                         "SYNOPSYS",
                         "\tback",
                         "DESCRIPTION",
                         "\tGo back to previous menu."
                         ])

    def help_run(self):
        """Print the 'run' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\trun -- Execute module's code.",
                         "SYNOPSYS",
                         "\trun",
                         "DESCRIPTION",
                         "\tCommand to run module's code " \
                            + "after the required options have been set."
                         ])

    def help_set(self):
        """Print the 'set' command documentation.

        Args:
          self: Reference to the instance of the class.
        """
        print "\n".join(["NAME",
                         "\tset -- Set module option.",
                         "SYNOPSYS",
                         "\tset <option> <value>",
                         "DESCRIPTION",
                         "\tThis command is used to set the module options."
                         ])
        self._show_options()

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
        options = [
            ["Option", "Description"],
            ["info", "Show module information"],
            ["options", "Show list of supported options by this module"]
        ]
        self._print_table(options)

    # ***************************************************************
    # HELPER methods
    # ***************************************************************

    def _show_info(self):
        """Display module metadata."""
        print "MODULE INFORMATION"
        print "Name: %s" % self.info["name"]
        print "Author: %s" % self.info["author"]
        print "Description: %s\n" % self.info["description"]
        self._show_options()

    def _show_options(self):
        """Display module supported options."""
        print "OPTIONS"
        self.info["options"].insert(0,
            ["Name", "Value", "Required", "Description"])
        self._print_table(self.info["options"])
        del self.info["options"][0]

    def get_option_index(self, option):
        """Get option index in metadata 'options' list.

        Args:
          option: The option to search for.
        """
        options = self.info["options"]
        index = 0
        for o in options:
            if option.lower() == o[0].lower():
                # Found option, return index
                return index
            index += 1
        # Option does not exist.
        return -1

    def get_option_value(self, option):
        """Get option value from metadata 'options' list.

        Args:
          option: The option to retrieve its value.
        """
        options = self.info["options"]
        index = self.get_option_index(option)
        if (index != -1):
            return options[index][1]
        # Option does not exist
        return None

    def is_option_valid(self, option):
        """Determine if given option is valid for the current module.

        Args:
          option: The option to search for.

        Returns:
          True if the option is valid for the current module.
          False otherwise.
        """
        options = self.info["options"]
        for o in options:
            if option == o[0].lower():
                return True
        return False

    def load_config_file(self):
        """Load option values from configuration file."""
        with open(self.config_file, "r") as config:
            for option in config:
                # Ignore comments
                option = option.strip()
                if (len(option) == 0):
                    continue
                if (option[0] != "#"):
                    option_value = re.split(r'=', option, 1)
                    if len(option_value) != 2:
                        continue
                    self.set_option_value(option_value[0].strip(),
                        option_value[1].strip())

    def set_option_value(self, option, value):
        """Method to set a module option.

        Args:
          self: Reference to the instance of the class.
          option: The option to set
          value: The value that the option will store.

        Returns:
          True if the option is valid and was set properly.
          False otherwise.
        """
        # Get option index from module's metadata
        opt_index = self.get_option_index(option)
        if (opt_index != -1):
            # Valid option
            if (value == "\"\"" or value == "''"):
                # Unset the option
                value = ""
            elif (value.lower() == "true"):
                value = True
            elif (value.lower() == "false"):
                value = False
            # Store the option's value in the module's metadata
            self.info["options"][opt_index][1] = value
            return True
        # Option not found in module's metadata.
        return False

class IOSModule(BaseModule):
    """Base class for the framework's iOS modules.

    This class extends BaseModule and implements common functionality
    that can be reused by new iOS modules.

    Attributes:
      backup_dir: A string that stores the path to the iOS backup.
      contacts_db_path: A string that stores the path to the
                        contacts DB within the iOS backup.
      require_contacts: A boolean indicating if the module requires
                        access to the contacts (address book) DB.
      require_sms: A boolean indicating if the module requires
                    access to the iMessage/SMS DB.
      sms_db_path: A string that stores the path to the iMessage/SMS
                    DB within the iOS backup.
    """
    def __init__(self, config_file = None):
        """Initializes the Module.

        Sets default values for class attributes.
          Subclasses can override these defaults.
        Adds BACKUP_DIR as a required option for iOS modules.
        """
        BaseModule.__init__(self, None)
        # Adding iOS Backup Directory as a required
        # option for any iOS Module.
        self.info["options"].insert(0,
            ["BACKUP_DIR", "", True, "Path to iOS Backup"])
        self.require_contacts = False
        self.require_sms = False
        self.contacts_db_path = ""
        self.sms_db_path = ""
        self.backup_dir = ""
        # Load general iOS settings
        # This configuration file is where the
        # path to the iOS backup can be set for all
        # iOS modules
        self.config_file = self.app_path + "/" \
            + "lib/modules/mobile/ios/ios.conf"
        self.load_config_file()
        if (config_file is not None):
            # Loading module specific options
            # If the module specific configuration file
            # sets a path to the iOS backup, it will
            # overwrite the path set in the
            # general ios.conf file.
            self.config_file = self.app_path + "/" + config_file
            self.load_config_file()

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def do_run(self, line):
        """Implementation of the 'run' command.

        Args:
          self: Reference to the instance of the class.
          line: The arguments to the 'run' command.
                Not used by the 'run' command.
        """
        # Validate iOS Backup Directory
        backup_dir = self.get_option_value("backup_dir")
        if (not os.path.isdir(backup_dir)):
            # Path does not exist
            print "Error: '%s' is not a directory." % backup_dir
            return
        self.backup_dir = backup_dir

        if (self.require_contacts):
            # The module needs to use the contacts database
            # Check if contacts database exists
            self.contacts_db_path = backup_dir + "/" \
                + iosconstants.Backup.CONTACTS_DB_FILE_NAME_HASH
            if (not os.path.isfile(self.contacts_db_path)):
                print "Error: iOS Contacts DB does not exist " \
                    + "in the BACKUP_DIR provided."
                return

        if (self.require_sms):
            # The module needs to use the iMessage/SMS database
            # Check if iMessage/SMS database exists
            self.sms_db_path = backup_dir + "/" \
                + iosconstants.Backup.MESSSAGES_DB_FILE_NAME_HASH
            if (not os.path.isfile(self.sms_db_path)):
                print "Error: iOS Messages DB does not exist " \
                    + "in the BACKUP_DIR provided."
                return

        # All validations passed, call
        # BaseModule's implementation of do_run()
        # for validations not specific to iOS and
        # to run the module's code.
        BaseModule.do_run(self, line)
