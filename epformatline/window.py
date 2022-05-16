from sys import exit
from tkinter import Button, Entry, Label, StringVar, Tk, NSEW, scrolledtext, END

from epformatline.worker import translate


class FormatGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("E+ Format Generator")
        self.root.geometry('1600x150')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.lbl = Label(self.root, text="Enter original concatenated string code: ")
        self.lbl.grid(column=0, row=0, sticky=NSEW, padx=2, pady=2)
        self.text_area = scrolledtext.ScrolledText(self.root, width=160, height=3)
        self.text_area.grid(column=1, row=0, sticky=NSEW, padx=2, pady=2)

        btn = Button(self.root, text="Translate", command=self.click_translate)
        btn.grid(column=0, row=1, columnspan=2, sticky=NSEW, padx=600, pady=2)

        note = Label(self.root, text="Translated string: Ctrl-C will copy: ")
        note.grid(column=0, row=2)
        self.out_text_var = StringVar(self.root, value='<translated string>')
        self.txt_out = Entry(self.root, textvariable=self.out_text_var)
        self.txt_out.grid(column=1, row=2, sticky=NSEW, padx=2, pady=2)

        btn = Button(self.root, text="Copy Output Box Text to Clipboard", command=self.copy_contents)
        btn.grid(column=0, row=3, columnspan=2, sticky=NSEW, padx=600, pady=2)

        self.root.protocol("WM_DELETE_WINDOW", self.client_exit)
        self.root.mainloop()

    def click_translate(self):
        out = translate(self.text_area.get("1.0", END))
        self.out_text_var.set(out)

    def copy_contents(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.out_text_var.get())
        self.root.update()  # now it stays on the clipboard after the window is closed

    # noinspection PyMethodMayBeStatic
    def client_exit(self):
        exit()
