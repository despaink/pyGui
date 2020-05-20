import tkinter as tk

#initialize window
window = tk.Tk()
window.geometry('350x400')

#add widgets
rocksLabel = tk.Label(
    text="Python Rocks!",
     bg="#34A2FE",
     width=10,
     height=5,
     )

rocksLabel.pack()

clickMeButton = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    ) 

clickMeButton.pack()

entryLabel= tk.Label(text="Name")
entry = tk.Entry()

entryLabel.pack()
entry.pack()

#build/display window with the attached widgets
window.mainloop()