# -*- coding: utf-8 -*-
"""VocabTool GUI module

This is the GUI module of 'VocabTool'.
It is written with Tcl/Tk
It connects the GUI with core.
"""

# Standard library
import tkinter as tk
import tkinter.ttk as ttk

# Local modules
import core


# Main frame
class VocabTool(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Vocab Tool")

        # Mainframe
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # Search input
        self.word_text = tk.StringVar()
        word_entry = ttk.Entry(mainframe,
                               width=60,
                               textvariable=self.word_text)
        word_entry.grid(column=2, row=1, columnspan=4)

        # Buttons
        self.language = tk.StringVar()
        language_list = [("Eng", "en"), ("Jap", "jp"), ("Deu", "de")]
        ttk.Button(mainframe,
                   text="Search",
                   command=self.lookup).grid(column=6, row=1)
        ttk.Button(mainframe,
                   text="To Database",
                   command=self.add_to_database).grid(column=6, row=4,)
        for i in range(len(language_list)):
            button = ttk.Radiobutton(mainframe,
                                     variable=self.language,
                                     text=language_list[i][0],
                                     value=language_list[i][1])
            button.grid(column=i + 2, row=2)
            if i == 0:
                button.state(["selected"])
                self.language.set(language_list[0][1])

        # Text displays
        self.word_display = tk.Text(mainframe, width=60, height=30)
        self.word_display.grid(column=2, row=4, columnspan=4, rowspan=3)
        self.word_display.config(state=tk.DISABLED)
        word_list = tk.Listbox(mainframe, width=10, height=20)
        word_list.grid(column=1, row=4, rowspan=2)
        s = ttk.Scrollbar(mainframe,
                          orient=tk.VERTICAL,
                          command=word_list.yview)
        word_list['yscrollcommand'] = s.set

        # Menubar
        # Create meanubar
        self.option_add("*tearOff", False)
        menubar = tk.Menu(self)
        menu_f = tk.Menu(menubar)
        menu_a = tk.Menu(menubar)
        menu_f_ex = tk.Menu(menu_f)

        # Setup menubar
        self["menu"] = menubar
        menubar.add_cascade(menu=menu_f, label="File")
        menubar.add_cascade(menu=menu_a, label="About")
        menu_f.add_cascade(menu=menu_f_ex, label="Export as PDF")
        menu_f_ex.add_command(label="Word and explanation",
                              command=lambda: self.ex("we"))
        menu_f_ex.add_command(label="Word only",
                              command=lambda: self.ex("w"))
        menu_f_ex.add_command(label="Explanation Only",
                              command=lambda: self.ex("e"))

    def lookup(self):
        """Look up the word in the input box"""

        # TODO: Implement tagged display <RihanW>
        # Pass the request to core
        lookup_result = core.lookup_word(self.word_text.get(),
                                         self.language.get())

        # Show result
        show = ""
        for super_entry in lookup_result:
            show = show + super_entry.show_with_style()
        if show == "":
            show = "No reponse"
        self.update_word_display(show)

    def add_to_database(self):
        """Add the current entry to database"""

        # TODO: Implement function:VocabTool.add_to_database <RihanW>

        place_holder = "Add to atabase not yet implemented"
        self.update_word_display(place_holder)

    def ex(self, mode):
        """Export PDF"""

        # TODO: Implement function:VocabTool.ex <RihanW>
        place_holder = "Export not yet implemente"
        self.update_word_display(place_holder)

    def update_word_display(self, text):
        """Update the content in self.word_display"""

        self.word_display.config(state=tk.NORMAL)
        self.word_display.delete("1.0", tk.END)
        self.word_display.insert(tk.END, text)
        self.word_display.config(state=tk.DISABLED)


main = VocabTool()
main.mainloop()
