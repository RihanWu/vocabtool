# -*- coding: utf-8 -*-
"""VocabTool core module

This is the core module of 'VocabTool'.
It connects the other modules with each other.
"""
# Standard module
import json

# Local modules
import database
import generate


class ConfigError(Exception):
    """Exception raised for errors regarding configuration"""

    def __init__(self, message):
        self.message = message


class VocabTool():
    """The core component of Vocabtool

    Attributes:
        config (dict): Configutations
        loaded_dict (list): Loaded dictionary sources
    """

    def __init__(self, config_filename="config.json", config_string=None):
        """Initializer of VocabTool class

        Args:
            config_filename (Optional[str]): Name of configuration file
            config_string (Optional[str]): A string containning json formated
                configuration
        """

        self.load_config(config_filename, config_string)

    def load_config(self, config_filename=None, config_string=None):
        """Read config information from external file or string object

        Note:
            Only one of ``config_filename`` and ``config_string`` will be used.
            If both are present, ``config_string`` has a higher priority.

            If runs successfully, class attribute ``config`` and
            ``loaded_dict``  will be created

        Args:
            config_filename (Optional[str]): Name of configuration file
            config_string (Optional[str]): A string containning json formated
                configuration

        Raises:
            ConfigError
        """

        if config_string:
            try:
                self.config = json.loads(config_string)
            except json.decoder.JSONDecodeError:
                raise ConfigError("Configuration is not valid json format")
        elif config_filename:
            try:
                with open(config_filename, "rb") as handle:
                    content = handle.read().decode("utf-8")
                    self.config = json.loads(content)
            except FileNotFoundError:
                raise ConfigError("Invalid config file name")
            except UnicodeDecodeError:
                raise ConfigError("Config file is not encoded with utf-8")
            except json.decoder.JSONDecodeError:
                raise ConfigError("Configuration is not valid json format")
        else:
            raise ConfigError("No configuration provided")

        # Quick check of validity
        if ("dictionaries" not in self.config.keys() or
                len(self.config["dictionaries"]) == 0):
            raise ConfigError("Configuration contains no dictionary source")

        # Load enabled dictionary
        self.loaded_dict = list()  # (module, dictionary configuration)
        for dictionary in self.config:
            if dictionary["enable"]:
                self.loaded_dict.append((__import__("dict."+dictionary["id"],
                                                    fromlist=["*"]),
                                        dictionary))

    def read_config(self):
        pass

    def write_config(self):
        pass

    def look_up_word(self):
        pass

    def add_to_database(self):
        pass

    def read_from_database(self):
        pass

    def generate_LaTeX(self):
        pass


#
## Current word object
#current_word = list()
#
#
#def lookup_word(word_text, search_language, source_list=None):
#    """Look up word in sources as configed."""
#
#    # Reset current word
#    current_word = list()
#
#    # Lookup in loaded dictionaries
#    for source in loaded_dict:
#        if source[1]["lang"] == search_language:
#            if source_list:
#                if source[1]["id"] in source_list:
#                    current_word.append(source[0].lookup(source[1], word_text))
#            else:
#                current_word.append(source[0].lookup(source[1], word_text))
#
#    # Return to GUI
#    return current_word
#
#
#def add_to_database():
#    """Add the current word to database."""
#
#    response = database.add(current_word)
#
#
#def generate_pdf():
#    """Generate pdf that meets the requirement."""
#
#    response = generate.generate_pdf()
