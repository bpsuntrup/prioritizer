import tkinter as tk
from functools import partial

class StickyNote(object):
    def __init__(self, parent, onclick, myself=False):
        """Setting myself to True will pass 'self' to onclick callback as a first argument"""
        self.note = tk.Text(parent)
        if myself:
            self.note.bind("<Button-1>", onclick)
        else:
            self.note.bind("<Button-1>", partial(onclick, self))
        self.note.pack()

    def display(self, message):
        self.note.delete("1.0", tk.END)
        self.note.insert(tk.END, message)

def main():
    root = tk.Tk()
    left_text = StickyNote(root, partial(onclick, 'hi left'), myself=True)
    left_text.display('this is a note')
    right_text = StickyNote(root, partial(onclick, 'hi right'), myself=True)
    right_text.display('this is a note')

    root.mainloop()

def onclick(message, textbox, event):
    print(message, textbox)
    textbox.display(message)

if __name__ == "__main__":
    main()
