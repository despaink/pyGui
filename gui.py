import tkinter as tk

#initialize window
window = tk.Tk()
window.geometry('350x400')

#add widgets
entryLabel= tk.Label(text="Name")
entry = tk.Entry()

entryLabel.pack()
entry.pack()

dropOptions = ['_______','layer 1', 'layer 2',]
dropOptionLabel = tk.StringVar(window)
dropOptionLabel.set('_______')

dropDown = tk.OptionMenu(window, dropOptionLabel, *dropOptions)

dropDown.pack()

#methods
def change_option(*args):
    print(dropOptionLabel.get())

dropOptionLabel.trace('w', change_option)

#build/display window with the attached widgets
window.mainloop()