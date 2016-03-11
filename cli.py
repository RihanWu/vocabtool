"""CLI interface of vocabtool"""

# TODO: Implement CLI
# Import core component
import core

print("This is the CLI interface of  vocabtool")

while(True):
    word = input("Please input the word to lookup[English]:")
    result = core.lookup_word(word, "en")
    show = ""
    for super_entry in result:
        show = show + super_entry.show_no_style()
    if show == "":
        show = "No reponse"
    print(show)
