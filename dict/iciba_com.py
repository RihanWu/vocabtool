# -*- coding: utf-8 -*-
"""Module for iciba.com

Type: Webpage
URL: http://www.iciba.com/
"""

# Third-party library
import requests
from bs4 import BeautifulSoup

# Local module
if __name__ == "__main__":
    import base_class
else:
    from dict import base_class


class Iciba(base_class.SuperEntry):
    """Class for looking up a word from iciba.com"""

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def _store_info(self, div):
        """Parse the incoming div"""

        entry = base_class.Entry()
        entry.separate_storage = True

        # Pronounciation and sound information
        base_speak = div.find(attrs={"class": "base-speak"})
        if base_speak is None:
            pass
        else:
            span = base_speak.find_all("span")
            i = base_speak.find_all("i")
            for index, item in enumerate(span):
                text = item.get_text()
                entry.pronounciation.append((text[0],
                                             "[" +
                                             text[text.index("[") + 2: -2] +
                                             "]"))
                href = i[index]["onmouseover"]
                entry.sound.append(href[href.index("http"): -2])

        # Explanation
        # Take only the first list
        base_list = div.find_all(attrs={"class": "base-list switch_part"})
        if len(base_list) is not 0:
            items = base_list[0].find_all("li")
            # Different pos
            for item in items:
                copy_entry = base_class.Entry()
                copy_entry.pronounciation = entry.pronounciation
                copy_entry.sound = entry.sound
                copy_entry.pos = item.span.get_text()
                exp_text = [x.strip() for x in item.p.get_text().split(";")]
                copy_entry.explanation = ";".join(exp_text)
                self.entries.append(copy_entry)
        else:
            # There is only the keyword with no explanation
            self.valid = False

    def lookup(self):
        """Lookup word in iciba"""

        # Fetch data from the server
        response = requests.get(self.base_url + self.word_text)

        # Parse the webpage
        soup = BeautifulSoup(response.text, "lxml")
        divs = soup.find_all("div", attrs={"class": "info-article info-base"})

        if (len(divs) == 0):
            self.valid = False
        else:
            # Only parse first div
            self._store_info(divs[0])

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
    """The lookup function for iciba"""

    result = Iciba(dict_info, word_text)
    result.lookup()
    return result
