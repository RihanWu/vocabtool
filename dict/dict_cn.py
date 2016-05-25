# -*- coding: utf-8 -*-
"""Module for dict.cn

Type: Webpage
URL: http://dict.cn/
"""

import re

# Local module
from vocabtool.dict import base_class
import vocabtool.urllib_requests as requests

__parse_method__ = "re"


class DictCn(base_class.SuperEntry):
    """Class for looking up a word from dict.cn"""

    def __init__(self, dict_info, word_text):
        base_class.SuperEntry.__init__(self, dict_info["id"],
                                       dict_info["dictionary_name"],
                                       word_text)
        self.base_url = dict_info["base_url"]

    def _store_info(self, response):
        """Parse the incoming div

        entry.pronounciation    [(British/American, IPA), ...]
        entry.sound             [(href, href), ...]
        """

        entry_pat = """(?xs)
                       <div\sclass="word">
                       .*?
                       <\/div>
                       .*?
                       (?= <div\sclass="section\sdef">)"""
        explanation_pat = """(?xs)
                             (?<= <li>)         # match a li
                             (?: .*?<span>)
                             (?P<pos>.*?)       # the pos
                             (?= <\/span>)
                             .*?                # something in between
                             (?<= <strong>)     # the strong tag
                             (?P<exp>.*?)       # the explanation content
                             (?= <\/strong>)
                             (?: .*?<\/li>)"""
        pron_pat = """(?xs)
                      (?: <span>.*?)
                      (?P<style>\w)   # the British or American
                      (?: \s+<bdo.*?>)
                      (?P<pron>\[.*?\]) # the pronounciation
                      (?: <\/bdo>.*?naudio=")
                      (?P<fpron>.*?) # female pronounciation
                      (?: \?t=.*?naudio=")
                      (?P<mpron>.*?) # male pronounciation
                      (?: \?t=.*?<\/span>)"""

        entry_match = re.search(entry_pat, response)
        if entry_match:
            entry_text = entry_match.group(0)
            pron = re.findall(pron_pat, entry_text)
            explanation = re.findall(explanation_pat, entry_text)
            for item in explanation:
                entry = base_class.Entry()
                entry.pos = item[0]
                entry.explanation = item[1]
                for style, ipa, fpron, mpron in pron:
                    entry.pronounciation.append((style, ipa))
                    entry.sound.append((fpron, mpron))
                self.entries.append(entry)
        else:
            self.valid = False

    def lookup(self):
        """Lookup word in dict.cn"""

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
    """The lookup function for dict.cn"""

    result = DictCn(dict_info, word_text)
    result.lookup()
    return result
