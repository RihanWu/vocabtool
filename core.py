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

__version__ = "Waiting for assignment"


class ConfigError(Exception):
    """Exception raised for errors regarding configuration"""

    def __init__(self, message):
        self.message = message


class VocabTool():
    """The core component of Vocabtool

    Attributes:
        config_filename (str): Configuration file name
        config (dict): Configurations
        loaded_dict (list): Loaded dictionary sources
        current_word (list): Response from different sources for current word
    """

    def __init__(self, config_filename="config.json"):
        """Initializer of VocabTool class

        Args:
            config_filename (Optional[str]): Configuration file name
        """

        self.config_filename = config_filename
        self.config = None
        self.loaded_dict = list()  # (module, dictionary configuration)
        self.current_word = list()
        self.load_config()

    def load_config(self):
        """Read config information from external file or string object

        Note:
            If runs successfully, class attribute ``config`` and
            ``loaded_dict``  will be created

        Raises:
            ConfigError
        """

        try:
            with open(self.config_filename, "rb") as handle:
                content = handle.read().decode("utf-8")
                self.config = json.loads(content)
        except FileNotFoundError:
            raise ConfigError("Configuration file not found")
        except UnicodeDecodeError:
            raise ConfigError("Config file is not encoded with utf-8")
        except json.decoder.JSONDecodeError:
            raise ConfigError("Configuration is not valid json format")

        # Quick check of validity
        if ("dictionaries" not in self.config.keys() or
                len(self.config["dictionaries"]) == 0):
            raise ConfigError("Configuration contains no dictionary source")

        # Load enabled dictionary
        for dict_id, config in self.config["dictionaries"].items():
            if config["enable"]:
                self.loaded_dict.append((__import__("dict." + dict_id,
                                                    fromlist=["*"]),
                                        config))

    def read_config(self, config_path):
        """Read configuration from the loaded configuration object

        Args:
            config_path (str): Path connected by period

        Returns:
            A string representing the desired configuration
        """
        path = config_path.split(".")
        temp_config = self.config
        for i in path:
            if temp_config.get(i):
                temp_config = temp_config[i]
            else:
                raise ConfigError("Configuration does not exist")
        return temp_config

    def write_config(self, config_path, config_value):
        """Write value to specific configuration

        Args:
            config_path (str): Path connected by period
            config_value (str): Value to be writen
        """
        path = config_path.split(".")
        temp_config = self.config
        for i in path[:-1]:
            temp_config = temp_config[i]
        temp_config[path[-1]] = config_value

    def look_up_word(self, word_text, search_language, source_list=None):
        """Look up word in sources as configed.

        Args:
            word_text (str): The word or expression to be looked up
            search_language (str): Language to look in
            source_list (Optional[list]): If loaded, use these sources

        Returns:
            A list of responses from different sources
        """

        # Reset current word
        self.current_word = list()

        # Lookup in loaded dictionaries
        for source in self.loaded_dict:
            if source[1]["lang"] == search_language:
                if source_list:
                    if source[1]["id"] in source_list:
                        self.current_word.append(source[0].lookup(source[1],
                                                 word_text))
                else:
                    self.current_word.append(source[0].lookup(source[1],
                                             word_text))

        # Return
        return self.current_word

    def add_to_database(self):
        pass

    def read_from_database(self):
        pass

    def generate_latex(self):
        pass
