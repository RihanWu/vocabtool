"""Module for Merriam-Webster's Collegiate Dictionary with Audio

Type: API
URL: http://www.dictionaryapi.com/api/v1/references/collegiate/xml/
"""

import urllibRequests as requests
# Third-party library
from bs4 import BeautifulSoup

# Local module
if __name__ == "__main__":
    import base_class
else:
    from dict import base_class


class MerriamWebster(base_class.SuperEntry):
    """Class for looking up a word with Merriam Webster Dictionary API"""

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]
        self.key = dict_info["key"]

    def _store_info(self, single_entry):
        """Store the info of one single entry in to an Entry"""

        tag_containing_definition = ["dt", "ssl", "sn", "sd"]
        entry = base_class.Entry()
        entry.separate_storage = True
        entry.explanation = [[], []]
        for tag in single_entry.children:
            if (tag.name == "sound"):
                entry.sound = tag.wav.get_text()
            elif (tag.name == "pr"):
                entry.pronounciation = tag.get_text().strip()
            elif (tag.name == "fl"):
                entry.pos = tag.get_text()
            elif (tag.name == "def"):
                # Explore the "def" tag.
                for exp in tag.children:
                    # Sense number.
                    if (exp.name == "sn"):
                        # Primary sense number.
                        if (exp.get_text()[0].isdigit()):
                            exp_text = exp.get_text()[0]
                            for sib in exp.next_siblings:
                                # If the tag doesn't contain
                                # primary sense number but contains
                                # definition and secondary sense number
                                # instead, add it to exp_text
                                if (sib.name == "sn" and
                                        sib.get_text()[0].isdigit()):
                                    entry.explanation[0].append(exp_text +
                                                                "\n")
                                    break
                                elif (sib.name in tag_containing_definition):
                                    exp_text = " ".join([exp_text,
                                                        sib.get_text().
                                                        lstrip()])
                # Special case with no sense number
                if (tag.date.next_sibling.name == "dt"):
                    entry.explanation[0].append(tag.dt.get_text().lstrip(":"))

        return entry

    def lookup(self):
        """Lookup word in Merriam Webster dictionary"""

        # Fetch data from the server
        response = requests.get(self.base_url + self.word_text,
                                params={"key": self.key})

        # Parse the xml fetched
        soup = BeautifulSoup(response.text, "lxml")
        entries = soup.find_all("entry")

        if (entries):  # If the word is valid
            # The word only has one entry
            if (entries[0]["id"] == self.word_text):
                # Store entry info into result
                self.entries.append(self._store_info(entries[0]))
            # The word has more then one entry
            else:
                for entry in entries:
                    # If the entry is indeed one of the entries of the word
                    if (entry["id"].startswith(self.word_text + "[")):
                        self.entries.append(self._store_info(entry))
        else:  # If the word is no valid
            self.valid = False

    def show_no_style(self):
        """Generate displayable formated text"""

        formated_text = ""
        if (self.valid):
            formated_text = "".join([formated_text,
                                    "{}\n {}\n".format(self.source_name,
                                                       self.word_text)])
            for entry in self.entries:
                formated_text = "\n  ".join([formated_text,
                                             "Pronounciation:\{}\ \n POS:{}\n".
                                             format(entry.pronounciation,
                                                    entry.pos)])
                formated_text = "   ".join([formated_text,
                                           "   ".join(entry.explanation[0])])
        else:
            formated_text = self.source_name + "\n\n No result"
        return formated_text + "\n\n"

    # Not implemented yet
    show_with_style = show_no_style


def lookup(dict_info, word_text):
    """The lookup function for Merriam-Webster"""

    result = MerriamWebster(dict_info, word_text)
    result.lookup()
    return result
