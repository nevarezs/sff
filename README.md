Smartphone Forensics Framework
==============================

## Introduction
The Smartphone Forensics Framework (SFF) is a command-line tool written in Python 2.7.12 to perform forensics tasks on mobile devices. The framework provides the infrastructure on which modules can run to implement functionality for specific forensics tasks. In addition to the infrastructure code that is part of the framework, the first release of this project includes three modules out-of-the-box. These modules implement forensics tasks that interact with the iOS address book and messages database (i.e., where iMessages and SMS messages are stored).

The objective of creating a framework as opposed to individual tools for the specific functionality that the modules implement is to create the base for future enhancements and making future collaboration easier. Different people could focus on implementing different modules for specific mobile applications or even different mobile platforms.

## Dependencies / Requirements

The framework was developed on a Mac running OS X version 10.11.6 with Python version 2.7.12. The framework uses the following Python modules that need to be installed to be able to use the framework without errors:

pdfkit==0.5.0 (https://pypi.python.org/pypi/pdfkit) <br />
phonenumberslite==7.7.5 (https://pypi.python.org/pypi/phonenumberslite) <br />
terminaltables==3.1.0 (https://pypi.python.org/pypi/terminaltables) <br />
yattag==1.7.2 (https://pypi.python.org/pypi/yattag/) <br />

Each of the modules above can be installed using the command: <br />
`$ pip install <module>` <br />
e.g., `$ pip install pdfkit`

**IMPORTANT**: The pdfkit python module is a wrapper for the wkhtmltopdf utility. This utility needs to be installed as well. Otherwise, the python pdfkit module will not work properly (see https://pypi.python.org/pypi/pdfkit).

On the Mac, this can be installed using homebrew with homebrew cask: <br />
`$ brew cask install wkhtmltopdf` <br />
Homebrew reference: http://brew.sh/ <br />
Homebrew cask reference: https://caskroom.github.io/ <br />

## Framework
The Smartphone Forensics Framework consists of the following files:

#### sff.py
Entry point to the framework

#### output
Placeholder directory for html and pdf output.

#### lib
* common
  * db
    * sqlite
      * **db.py**: Implements functions to connect to and query sqlite databases.
  * mobile
    * ios
      * **contacts_helper.py**: Implements helper functions to interact with the iOS Address Book.
      * **iosconstants.py**: Implements iOS constants that are used by iOS modules.
* export
  * **html.py**: Implements functions to export output to HTML. Uses the yattag library (see requirements section).
  * **pdf.py**: Implements functions to export output to PDF. Uses the pdfkit library (see requirements section).
* modules
  * mobile
    * ios
      * native
        * contacts
          * **listcontacts.conf**: Configuration file for the contacts/list module (see Modules section for more details).
          * **listcontacts.py**: Implementation of the contacts/list module (see Modules section for more details).
        * messages
          * **extractconversations.conf**: Configuration file for the messages/extract_conversations module (see Modules section for more details).
          * **extractconversations.py**: Implementation of the messages/extract_conversations module (see Modules section for more details).
          * **listconversations.conf**: Configuration file for the messages/list module (see Modules section for more details).
          * **listconversations.py**: Implementation of the messages/list module (see Modules section for more details).
      * thirdparty: placeholder directory to add modules that implement functionality for third-party applications (e.g., Skype).

#### sff
* core
  * **base.py**: Implements the Forensics class that inherits from the ForensicsFramework class implemented in framework.py. The Forensics class contains the functionality of the main command-line menu/interpreter when the application starts. Implements the `show` and `use` commands and displays help.
  * **framework.py**: Implements the base ForensicsFramework class, that is the top-level class of the framework. Any functionality that can be accessed from any part of the application, should be implemented here.
  * **module.py**: Implements the BaseModule class. This is the top-level class for all modules that run on the framework. Implements code to load option values from a configuration file and implements the `run`, `set`, and `show` commands.

## Modules
The SFF includes the following three modules with this first release: <br />
1. `mobile/ios/native/contacts/list` <br />
2. `mobile/ios/native/messages/extract_conversations` <br />
3. `mobile/ios/native/messages/list` <br />

The three modules above inherit from the `IOSModule`, which is the base class for any module on the framework that needs to work with an iOS backup. The `IOSModule` class adds `BACKUP_DIR` as a required option. This value of `BACKUP_DIR` can be set in the top-level ios.conf configuration file, in the module specific configuration files, or at runtime by the user. The modules above support iOS 9+.

**NOTE**: Values for the module options can be included in the configuration files, or they can be specified at runtime using the set command.

### mobile/ios/native/contacts/list
This module can list the contact information from the iOS Address Book in the iOS Backup. The user can see the list of contacts in the application, or the user can export the output to an html or pdf file to analyze at a later point. The user can filter the contacts list by adding keywords that are used to search by name, organization, phone number, or email address. The user can also show or hide some columns in the output.

The options supported by this module are:
* **BACKUP_DIR**: path to the iOS Backup.
* **INCLUDE_ID**: whether to include the contact ID in the output as stored in the Address Book database or not.
* **INCLUDE_ORGANIZATION**: whether to include the ‘Organization’ column in the output or not.
* **KEYWORDS**: comma-separated list of keywords to filter the output.
* **OUTPUT_FILE_NAME_PREFIX**: the name (excluding the extension) of the file to create if the output is sent to an HTML or PDF document.
* **OUTPUT_FORMAT**: supported formats are stdout (for standard output), html, and pdf.
* **SPLIT_NAME**: if `True`, separate columns are used in the output for the first name and last name. If `False`, only one column is used which combines the first and last name.

### mobile/ios/native/messages/extract_conversations
This module can extract the content of specific conversations from the SMS/iMessage database stored in the iOS Backup. The user can specify a list of conversations to extract, the output format (i.e., stdout, html, or pdf), whether to show or hide some columns in the output, and whether to include contact information of the people in the conversation (if such information exists in the Address Book). The user can also specify keywords that are used to filter the output to only include messages that contain those keywords. Furthermore, the user can include a date range to filter the output to only include messages within the timeframe specified. The keywords and date filters can be combined to provide a more specific search functionality. Finally, by providing a range of all the conversations in the backup, the examiner can extract all the conversations in bulk. If html or pdf output is chosen, an individual file is created for each conversation that is part of the output when conversations are extracted in bulk.

The options supported by this module are:
* **BACKUP_DIR**: path to the iOS Backup.
* **CONVERSATION_IDS**: a comma-separated list of IDs of the conversations to extract. The IDs can be obtained using the `mobile/ios/native/messages/list module`. Values within the list can specify ranges by using a hyphen (e.g., 1-3,5,7-10).
* **END_DATE**: only include messages on or before this date. Specify date in the following format: YYYY-MM-DD.
* **INCLUDE_MESSAGE_ID**: whether to include the message ID for each message as stored in the messages database or not.
* **INCLUDE_SERVICE**: whether to include a column with the name of the service (e.g., SMS or iMessage) in the output or not.
* **INCLUDE_SUBJECT**: whether to include a column with the subject of the conversation (e.g., in a group chat) or not.
* **KEYWORDS**: comma-separated list of keywords to filter the output.
* **OUTPUT_FILE_NAME_PREFIX**: the name (excluding the extension) of the file to create if the output is sent to an HTML or PDF document.
* **OUTPUT_FORMAT**: supported formats are stdout (for standard output), html, and pdf.
* **SHOW_CONTACT_INFO**: if `True`, include the name of the people that are part of each conversation (except for the owner of the device) in the output.
* **START_DATE**: only include messages on or after this date. Specify date in the following format: YYYY-MM-DD.

### mobile/ios/native/messages/list
This module can show the list of conversations that are stored in the SMS/iMessage database. The output includes the list of phone numbers or email addresses of the people who are part of each conversation. If desired, the user can see the name of each person in the conversation by setting the SHOW_CONTACT_INFO option to True (assuming that the names associated with the given phone numbers or email addresses are stored in the Address Book).

The options supported by this module are:
* **BACKUP_DIR**: path to the iOS Backup.
* **OUTPUT_FILE_NAME_PREFIX**: the name (excluding the extension) of the file to create if the output is sent to an HTML or PDF document.
* **OUTPUT_FORMAT**: supported formats are `stdout` (for standard output), `html`, and `pdf`.
* **SERVICE**: Used to filter output to only include messages sent using a specific service. Valid options are: `any`, `imessage`, and `sms`.
* **SHOW_CONTACT_INFO**: if `True`, include the name of the people that are part of each conversation (except for the owner of the device) in the output.

## Developer Guide: Adding New Modules
The framework includes two base classes that can be used to reuse functionality in new modules:
* `BaseModule`: Top-level class for all modules in the framework.
* `IOSModule`: Base class for iOS modules in the framework.

After adding the module’s file and configuration file, the `do_use()` method in the Forensics class needs to be modified to load the new module. The module also needs to be added to the `_modules` list in the Forensics `__init__` method.

### Module Template for iOS Modules
```python
# The html module contains functions to generate html output
from lib.export import html
# The pdf module contains functions to generate pdf output
from lib.export import pdf
# IOS module is the Base class for modules that need an iOS Backups.
from sff.core.module import IOSModule

class Module(IOSModule):
    """The Module class implements the current module's code.

    mobile/ios/path/to/module (i.e., not the file system path)
        Module description.
    """
    info = {
        "name": "Module Name",
        "author": "Author",
        "description": "Module description",
        "options": [ # Exclude BACKUP_DIR, already added by IOSModule
            [
             "OPTION1", # Option Name
             "Default Value", # Value
             True, # Required Option
             "Option Description."
            ]
    }

    def __init__(self):
        """Initializes module.

        Set require_sms property to True so that IOSModule
        validates that the SMS/iMessage db is present in the backup directory.
        (Only if the SMS/iMessage db is needed by this module)

        Set require_contacts property to True so that IOSModule
        validates that the contacts db is present in the backup directory.
        (Only if the contacts db is needed by this module)
        """
        IOSModule.__init__(self,
            "relative/path/to/configuration/file/module.conf")
        self.require_contacts = True
        self.require_sms = True

    # ***************************************************************
    # COMMANDS
    # ***************************************************************

    def run(self):
        """Implement module functionality."""
        return

    # ***************************************************************
    # HELPER methods
    # ***************************************************************

    # Add any helper methods here
```

## Attributions
The following projects served as inspiration to come up with the navigation workflow of the SFF:
* Metasploit Framework (https://github.com/rapid7/metasploit-framework)
* Recon-ng (https://bitbucket.org/LaNMaSteR53/recon-ng)
* PowerShell Empire (https://github.com/adaptivethreat/Empire)

In addition, the modular architecture of the Recon-ng framework and their very good Development Guide was very helpful to come up with ideas to structure the code of the Smartphone Forensics Framework.

## References used during the development of the first release of the framework
“Getting Attached: Apple Messaging Attachments.” Internet: https://linuxsleuthing.blogspot.com/2015/01/getting-attached-apple-messaging.html

“Google Python Style Guide.” Internet: https://google.github.io/styleguide/pyguide.html

Heather Mahalik and Satish Bommisetty. Practical Mobile Forensics. Birmingham, UK: Packt Publishing, Ltd, 2016, pp. 119-189.

Mattia Epifani and Pasquale Stirparo. Learning iOS Forensics. Birmingham, UK: Packt Publishing, Ltd, 2016, pp. 125-172, 219-263.

“Messages.” Internet: https://www.theiphonewiki.com/wiki/Messages

“pymessage.” Internet: https://github.com/mjbrisebois/pymessage

Tim Proffitt. “Forensic Analysis on iOS Devices.” Internet: https://www.sans.org/reading-room/whitepapers/forensics/forensic-analysis-ios-devices-34092, Nov. 5, 2012 [Oct. 1, 2016]

“Who’s Texting? The iOS6 sms.db.” Internet: https://linuxsleuthing.blogspot.com/2012/10/whos-texting-ios6-smsdb.html
