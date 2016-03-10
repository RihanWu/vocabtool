"""This module contains base class for dictionary entry"""


class Entry():
    """Store info of a word that is one part of speech.

    Store pronounciation,sound,  part of speech, word explanation and
    example sentences about one word or expression.
    """

    def __init__(self):
        """Initialize a entry instance.

        pronounciation:
            [(tag, IPA), ...]

        sound:
            [herf, ..]

        separate_storage:
            Whether the explantion and the example sentences
            are stored side by side or separately.
            If true:[[explanation, ...],[example sentences, ...]]
            If false:[[explanation,example sentences], ...]
        """

        # FIXME: pronouciation datastructure as list
        self.pronounciation = []
        self.sound = []
        self.pos = ""
        self.separate_storage = True
        self.explanation = []


class SuperEntry():
    """Store explanations of a word that may be different part of speech.

    Store word text, source and entries of a word.
    """

    def __init__(self, source, source_name, word_text):
        """Initialize a SuperEntry instance.

        valid:      Whether there is valid response from the dictionary
        source:     Source of the SuperEntry
        source_name:Name of the source of the SuperEntry
        wordText:   Text of the word or expression
        entries:    List of entries
        """

        self.valid = True
        self.source = source
        self.source_name = source_name
        self.word_text = word_text
        self.entries = []

    def show_no_style(self):
        """Generate displayable formated text with out style sheet"""

        pass

    def show_with_style(self):
        """Generate displayable formated text with style sheet"""

        pass

    def dbformat(self):
        """Generate structured data to be stored in database"""

        pass
