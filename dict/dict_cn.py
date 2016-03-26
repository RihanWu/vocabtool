# -*- coding: utf-8 -*-
"""Module for dict.cn

Type: Webpage
URL: http://dict.cn/
"""

# Third-party library
import requests
from bs4 import BeautifulSoup

# Local module
if __name__ == "__main__":
    import base_class
else:
    from dict import base_class


class DictCn(base_class.SuperEntry):
    """Class for looking up a word from dict.cn"""

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def _store_info(self, div_word):
        """Parse the incoming div

        entry.pronounciation    [(British/American, IPA), ...]
        entry.sound             [(href, href), ...]
        """

        entry = base_class.Entry()
        entry.separate_storage = True

        # Pronounciation and sound information
        phonetic = div_word.find("div", attrs={"class": "phonetic"})
        spans = phonetic.find_all("span")
        for span in spans:
            entry.pronounciation.append(tuple(span.get_text().split()))
            hrefs = tuple(["http://audio.dict.cn/" + x["naudio"]
                           for x in span.find_all("i")])
            entry.sound.append(hrefs)

        # Explanation
        dict_basic_ul = div_word.find("ul", attrs={"class": "dict-basic-ul"})
        for child in dict_basic_ul.find_all("li"):
            if child.get("style") is None:
                copy_entry = base_class.Entry()
                copy_entry.pronounciation = entry.pronounciation
                copy_entry.sound = entry.sound
                copy_entry.pos = child.span.get_text()
                copy_entry.explanation = child.strong.get_text()
                self.entries.append(copy_entry)

    def lookup(self):
        """Lookup word in dict.cn"""

        # Fetch data from the server
        response = requests.get(self.base_url + self.word_text)

        # Parse the webpage
        soup = BeautifulSoup(response.text, "lxml")
        div_word = soup.find("div", attrs={"class": "word"})

        if (len(div_word.find_all("div")) is 0):
            self.valid = False
        else:
            self._store_info(div_word)

    def show_no_style(self):
        """Generate displayable formated text"""

        formated_text = ""
        if (self.valid):
            formated_text = "".join([formated_text,
                                    "{}\n {}\n".format(self.source_name,
                                                       self.word_text)])
            for entry in self.entries:
                pron = " ".join(["".join(x) for x in entry.pronounciation])
                formated_text = "\n  ".join([formated_text,
                                             "Pronounciation:{} \n  POS:{}\n".
                                             format(pron,
                                                    entry.pos)])
                formated_text = "   ".join([formated_text,
                                           entry.explanation])
        else:
            formated_text = self.source_name + "\n\n No result"
        return formated_text + "\n\n"

    # Not implemented yet
    show_with_style = show_no_style


def lookup(dict_info, word_text):
    """The lookup function for dict.cn"""

    result = DictCn(dict_info, word_text)
    result.lookup()
    return result
