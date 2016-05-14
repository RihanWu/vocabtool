# -*- coding: utf-8 -*-
"""Module for iciba.com

Type: Webpage
URL: http://www.iciba.com/
"""

import re
from urllib.error import HTTPError

# Local module
from vocabtool.dict import base_class
import vocabtool.urllib_requests as requests

__parse_method__ = "re"


class Iciba(base_class.SuperEntry):
    """Class for looking up a word from iciba.com"""

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def _store_info(self, response):
        entry_pat = """(?xs)
                        <ul\sclass='base-list.*?>
                        .*?
                        <\/ul>"""
        explanation_pat = """(?xs)
                             (?<= <span\sclass='prop'>) # match a prop class span
                             (?P<prop>.*?)   # the prop content
                             (?= <\/span>)   # end of the span
                             .*?             # something in between
                             (?<= <p>)       # the p tag
                             (?P<p>.*?)      # the content in p
                             (?= <\/p>)"""
        pron_pat = """(?xs)
                    (?<= <span>) # match a prop class span
                    (?P<pron>\w?\s\[.*?\])   # the prop content
                    (?= <\/span><i\sclass='new-speak-step'\s
                    onmouseover="displayAudio\(')   # end of the span
                    (?: .*?)       # the p tag
                    (?P<url> http.*?\.mp3)      # the content in p
                    (?: .*?<\/i>)"""

        entry_match = re.search(entry_pat, response)
        if entry_match:
            pron = re.findall(pron_pat, response)
            explanation = re.findall(explanation_pat, entry_match.group(0))
            for item in explanation:
                entry = base_class.Entry()
                entry.pos = item[0]
                entry.explanation = ";".join([x.strip() for x in item[1].split(";")])
                for pron_string, sound in pron:
                    entry.pronounciation.append((pron_string[0],
                                                "".join(pron_string[1:].split())))
                    entry.sound.append(sound)
                self.entries.append(entry)
        else:
            self.valid = False

    def lookup(self):
        """Lookup word in iciba"""

        # Fetch data from the server
        try:
            response = requests.get(self.base_url + self.word_text)
            self._store_info(response)
            self.error_code = None
        except HTTPError as error:
            self.valid = False
            self.error_code = str(error.code)

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
        elif self.error_code:
            formated_text = self.source_name + "\n\n Error:" + self.error_code
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
