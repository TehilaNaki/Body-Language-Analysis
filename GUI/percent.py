'''# Python program to create
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog


# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)


# Create the root window
window = Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("500x500")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="File Explorer using Tkinter",
                            width=100, height=4,
                            fg="blue")

button_explore = Button(window,
                        text="Browse Files",
                        command=browseFiles)

button_exit = Button(window,
                     text="Exit",
                     command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=2)

button_exit.grid(column=1, row=3)

# Let the window wait for any events
window.mainloop()'''
import time
import tkinter as tk
import tkinter.ttk as ttk

tuple_1 = tuple(range(1, 25))


def progress_bar_func(style, progress_bar, sequence):
    root.after(500, update_progress_bar, style, progress_bar, 1, len(sequence))


def update_progress_bar(style, progress_bar, num, limit):
    if num <= limit:
        percentage = round(num / limit * 100)  # Calculate percentage.
        progress_bar.config(value=num)
        style.configure('text.Horizontal.TProgressbar', text='{:g} %'.format(percentage))
        num += 1
        root.after(500, update_progress_bar, style, progress_bar, num, limit)


root = tk.Tk()
root.geometry("300x300")

style = ttk.Style(root)
style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
style.configure('text.Horizontal.TProgressbar', text='0 %')

progress_bar = ttk.Progressbar(root, style='text.Horizontal.TProgressbar', length=200,
                               maximum=len(tuple_1), value=0)
progress_bar.pack()

progress_button = tk.Button(root, text="start",
                            command=lambda: progress_bar_func(style, progress_bar, tuple_1))
progress_button.pack()

root.mainloop()
